(ns dissections
    (:require clojure.contrib.math)
    (:require clojure.string)
    (:require clojure.contrib.string)
    (:use     [clojure.set :only (union)])
    (:use     [clojure.contrib.duck-streams :only (read-lines)]))

; An element a + b*sqrt(3) in QQ(sqrt(3)) is represented as the list [a b]

(defn length2? [x]
  (= (count x) 2))

(defn qq3prod [x y]
  "Product x*y where x, y are in QQ(sqrt(3))."
  (let [[xa xb] x
	    [ya yb] y]
    (assert (length2? x))
    (assert (length2? y))
    [(+ (* xa ya) (* 3 xb yb)) (+ (* xa yb) (* xb ya))]))

(defn qq3div-by-scalar [x y]
  "Computes x/y where x is in QQ(sqrt(3)) and y is an integer."
  (let [[xa xb] x]
    (assert (length2? x))
    (assert (integer? y))
    [(/ xa y) (/ xb y)]))

(defn qq3add [x y]
  "Computes x + y where x, y are in QQ(sqrt(3))."
  (let [[xa xb] x
	    [ya yb] y]
    (assert (length2? x))
    (assert (length2? y))
    [(+ xa ya) (+ xb yb)]))

(defn qq3sub [x y]
  "Computes x - y where x, y are in QQ(sqrt(3))."
  (let [[xa xb] x
	    [ya yb] y]
    (assert (length2? x))
    (assert (length2? y))
    [(- xa ya) (- xb yb)]))

(assert (= (qq3add  [1 1] [3 4]) [4 5]))
(assert (= (qq3prod [1 2] [3 0]) [3 6]))
(assert (= (qq3prod [1 2] [0 3]) [18 3]))
(assert (= (qq3prod [1 2] [5 9]) [59 19]))

(defn rotate-equilateral [x1 y1]
  "Suppose that the point (x1, y1) is in the unit equilateral triangle
   with side along the x-axis from 0 to 1. This function rotates the point
   x1,y1 about the centre of the equilateral triangle anticlockwise by angle 2*pi/3."
  (letfn [(tmp-fn-1 [x1 z] (qq3sub z (qq3prod [1/2 0] x1)))
          (tmp-fn-2 [y1 z] (qq3sub z (qq3prod [1/2 0] y1)))]
    (let [x2 (->> [-1/2 0]
                  (qq3prod [0 1])
                  (qq3prod y1)
                  (tmp-fn-1 x1)
                  (qq3add [1 0]))
          y2 (->> [1/2 0]
                  (qq3prod [0 1])
                  (qq3prod x1)
                  (tmp-fn-2 y1))]
      [x2 y2])))

(defn rotate-equilateral-inverse [x1 y1]
  (let [[x2 y2] (rotate-equilateral x1 y1)]
    (rotate-equilateral x2 y2)))

(assert (= (rotate-equilateral [0 0]   [0 0])   [[1 0]   [0 0]]))
(assert (= (rotate-equilateral [1 0]   [0 0])   [[1/2 0] [0 1/2]]))
(assert (= (rotate-equilateral [1/2 0] [0 1/2]) [[0 0]   [0 0]]))

(let [[x y] (rotate-equilateral [0 0] [0 0])]
  (assert (= (rotate-equilateral-inverse x y) [[0 0] [0 0]])))

(defn reflect1 [x y]
  "Reflect along the line x = 1/2."
  (letfn [(negate-x-coordinate [[x, y]]
            [(- x) y])]
    (let [flipped-x (-> x
                        (qq3add [-1/2 0])
                        (negate-x-coordinate)
                        (qq3add [1/2 0]))]
      (list flipped-x y))))

(assert (= (reflect1 [1/4 0] [0 0]) [[3/4 0] [0 0]]))

(defn reflect2 [x1 y1]
  "The reflection of the equilateral triangle that fixes (0, 0)."
  (->> [x1 y1]
       (apply rotate-equilateral-inverse)
	   (apply reflect1)
       (apply rotate-equilateral)))

(assert (= (reflect2 [0 0] [0 0]) [[0 0] [0 0]]))
(assert (= (reflect2 [1 0] [0 0]) [[1/2 0] [0 1/2]]))

(defn reflect3 [x1 y1]
  "The reflection of the equilateral triangle that fixes (1, 0)."
  (->> [x1 y1]
       (apply rotate-equilateral)
	   (apply reflect1)
       (apply rotate-equilateral-inverse)))

(assert (= (reflect3 [1 0] [0 0]) [[1 0] [0 0]]))
(assert (= (reflect3 [0 0] [0 0]) [[1/2 0] [0 1/2]]))

(defn split [s]
  "This is similar to Python's .split() function on strings."
  (remove clojure.string/blank? (clojure.contrib.string/split #"[ ]" s)))

(defn line-to-numbers [line]
  "Parse a string consisting of integers separated by spaces."
  (map read-string (split line)))

; Similar to Common Lisp's incf.
(defmacro incf [variable]
  `(var-set ~variable (inc (var-get ~variable))))

(defn find-pivot [matrix start initial-lead]
  (let [nr-rows   (count matrix)
        nr-cols   (count (first matrix))]
    (with-local-vars [i     start
                      lead  initial-lead]
      (while (= 0 (aget matrix (var-get i) (var-get lead)))
        (incf i)
        (when (= (var-get i) nr-rows)
          (var-set i start)
	      (incf lead)
		  (when (= (var-get lead) nr-cols)
            (assert false) ; see comment below
            nil)))
      (list (var-get i) (var-get lead)))))

; The (assert false) is for the case where the Common Lisp code does
; a return-from to pop out of the entire algorithm:
; 
; (when (= lead column-count)
;    (return-from convert-to-row-echelon-form matrix))))
;
; Clojure doesn't have a return-from...

(defn swap-rows [matrix r1 r2]
  (dotimes [c (count (first matrix))]
    (let [tmp (aget matrix r2 c)]
      (aset matrix r2 c (aget matrix r1 c))
      (aset matrix r1 c tmp))))

(defn divide-row [matrix r value]
  (dotimes [c (count (first matrix))]
    (aset matrix r c (/ (aget matrix r c) value))))

(defn convert-to-row-echelon-form [matrix]
  (let [row-count     (count matrix)
        column-count  (count (first matrix))]
    (with-local-vars [lead 0]
      (dotimes [r row-count]
        (when (> column-count (var-get lead))
          (let [[i nlead] (seq (find-pivot matrix r (var-get lead)))]
            (var-set lead nlead)
            (swap-rows matrix i r)
            (divide-row matrix r (aget matrix r (var-get lead)))
            (dotimes [k row-count]
              (when (not= k r)
                (let [scale (aget matrix k (var-get lead))]
                  (dotimes [c column-count]
                    (aset matrix k c (- (aget matrix k c) (* scale (aget matrix r c))))))))
            (incf lead)))))))

(defn row-with-positions-set [row-length positions-and-values]
  (let [row (make-array Object row-length)]
    (dotimes [i row-length]
      (aset row i 0))
    (doseq [[i value] positions-and-values]
      (aset row i value))
    row))

(defn identity-element-equations [identity-triple nr-rows nr-cols nr-syms]
  (let [[id-row id-col id-sym] identity-triple
        m (+ nr-rows nr-cols nr-syms 1)]
    [(row-with-positions-set m [[id-row 1]])                                      ; r_{id-row} = 0
     (row-with-positions-set m [[(+ id-col nr-rows) 1]])                          ; c_{id-col} = 0
     (row-with-positions-set m [[(+ id-sym nr-rows nr-cols) 1] [(- m 1) 1]])]))   ; s_{id-sym} = 1

(defn normal-element-equations [triple nr-rows nr-cols nr-syms]
  (let [[r c s] triple
        m (+ nr-rows nr-cols nr-syms 1)]
    (row-with-positions-set m [[r 1] [(+ c nr-rows) 1] [(+ s nr-rows nr-cols) -1]])))

(defn equations-from-trade [trade identity-triple nr-rows nr-cols nr-syms]
  ; For full details on how these equations are constructed, see
  ; Drapal and Hamalainen, "An enumeration of equilateral triangle dissections", http://arxiv.org/abs/0910.5199
  (concat
    (for [triple (filter #(not= identity-triple %) trade)] (normal-element-equations triple nr-rows nr-cols nr-syms))
    (identity-element-equations identity-triple nr-rows nr-cols nr-syms)))

(defn last-column [matrix]
  (let [nr-rows (count matrix)
        nr-cols (count (first matrix))
        last-col (- nr-cols 1)]
    (vec (for [row (range nr-rows)]
           (aget matrix row last-col)))))

(defn triangle-size [pt1 pt2 pt3]
  (cond (= (first pt1)  (first pt2))  (clojure.contrib.math/abs (- (second pt1) (second pt2)))
        (= (second pt1) (second pt2)) (clojure.contrib.math/abs (- (first pt1)  (first pt2)))
        :else                         (triangle-size pt2 pt3 pt1)))

(assert (= (triangle-size [0 0] [1 0] [0 1]) 1))
(assert (= (triangle-size [1 0] [0 1] [0 0]) 1))
(assert (= (triangle-size [1 1] [1 1] [1 1]) 0))

(defn point-to-4list [point]
  (assert (length2? point))
  (let [[pt1 pt2] point]
    (assert (length2? pt1))
    (assert (length2? pt2))
    (vec (concat pt1 pt2))))

(defn apply-transformation [t-fn points]
  (for [xy points]
    (vec (apply t-fn xy))))

(defn right-angle-to-equilateral [points]
  (for [xy points]
    (let [[x y] xy
          val-x (qq3add (qq3div-by-scalar y 2) x)         
		  val-y (qq3div-by-scalar (qq3prod '(0 1) y) 2)]
            [val-x val-y])))

(defn canonical-signature [points]
  (letfn [(csig [points] (vec (apply concat (sort (map point-to-4list points)))))]
    (let [equilateral (right-angle-to-equilateral points)
          images (concat [(csig equilateral)]
                         (for [trans-fn [reflect1 reflect2 reflect3 rotate-equilateral rotate-equilateral-inverse]]
                           (csig (apply-transformation trans-fn equilateral))))]
      (first (sort images)))))

(defn bgen [lines]
  (lazy-seq
    (when (seq lines)
      (let [[nr-rows nr-cols nr-syms] (line-to-numbers (first lines))
            nr-elements               (first (line-to-numbers (second lines)))
            T1                        (map line-to-numbers (take nr-elements (drop 2 lines)))
            T2                        (map line-to-numbers (take nr-elements (drop (+ 3 nr-elements) lines)))]
        (cons {:nr-rows nr-rows :nr-cols nr-cols :nr-syms nr-syms :nr-elements nr-elements :T1 T1 :T2 T2} (bgen (drop (+ 3 (* 2 nr-elements)) lines)))))))

(defn is-separated-solution? [M nr-rows nr-cols nr-syms]
  (let [nr-unique-row-bits  (count (set (subvec M 0 nr-rows)))
        nr-unique-col-bits  (count (set (subvec M nr-rows (+ nr-rows nr-cols))))
        nr-unique-sym-bits  (count (set (subvec M (+ nr-rows nr-cols))))]
    (and (= nr-rows nr-unique-row-bits)
         (= nr-cols nr-unique-col-bits)
         (= nr-syms nr-unique-sym-bits))))

(defn inject-into-qq3 [x]
  [x 0])

(defn flatten-one-level [x]
  (lazy-seq
    (when (seq x)
      (let [x0 ((first x) 0)
            x1 ((first x) 1)
            x2 ((first x) 2)]
        (cons x0 (cons x1 (cons x2 (flatten-one-level (rest x)))))))))

(defn solve-dissection-equations [nr-rows nr-cols nr-syms T1 T2 identity-triple-in-T1]
  (def tmp-array (into-array Object (equations-from-trade T1 identity-triple-in-T1 nr-rows nr-cols nr-syms)))
  (convert-to-row-echelon-form tmp-array)
  (let [M (last-column tmp-array)]
    (when (is-separated-solution? M nr-rows nr-cols nr-syms)
      (vec (set (flatten-one-level (for [[r c s] T2]
                                     (let [w1 (nth M r)                      ; w1 = self.M[r]
		                                   w2 (nth M (+ c nr-rows))          ; w2 = self.M[c + self.row_max]
		                                   w3 (nth M (+ s nr-rows nr-cols))  ; w3 = self.M[s + self.row_max + self.col_max]

		                                   pt1 [w2 w1]         ; pt1 = (w2, w1)
		                                   pt2 [w2 (- w3 w2)]  ; pt2 = (w2, w3 - w2)
		                                   pt3 [(- w3 w1) w1]  ; pt3 = (w3 - w1, w1)

		                                   fpt1 (map inject-into-qq3 pt1)
		                                   fpt2 (map inject-into-qq3 pt2)
		                                   fpt3 (map inject-into-qq3 pt3)]
                                       [fpt1 fpt2 fpt3]))))))))

(defn signatures [nr-rows nr-cols nr-syms T1 T2]
  (for [identity-triple T1]
    (let [soln (solve-dissection-equations nr-rows nr-cols nr-syms T1 T2 identity-triple)]
      (when (= (+ (count T1) 2) (count soln))
        (canonical-signature soln)))))

(comment

  This blob will count separated dissections, as opposed to simply
  outputting canonical signatures for later counting using uniq/sort-n.

(doseq [i (concat [4] (range 6 12))]
  (print i)
  (print " ")
  (println (count (apply union (for [{:keys [nr-rows nr-cols nr-syms T1 T2]} (bgen (read-lines (str "../spherical_bitrade_generator/spherical_bitrades_" i)))]
                                 (->> (concat (signatures nr-rows nr-cols nr-syms T1 T2)
                                              (signatures nr-rows nr-cols nr-syms T2 T1))
                                      (remove nil?)
                                      (set)))))))
)

(doseq [i (concat [4] (range 6 13))]
  (binding [*out* (java.io.FileWriter. (str "separated_test_out_" i))]
    (doseq [{:keys [nr-rows nr-cols nr-syms T1 T2]} (bgen (read-lines (str "../spherical_bitrade_generator/spherical_bitrades_" i)))]
      (doseq [sig (signatures nr-rows nr-cols nr-syms T1 T2)]
        (prn sig))
      (doseq [sig (signatures nr-rows nr-cols nr-syms T2 T1)]
        (prn sig)))))










