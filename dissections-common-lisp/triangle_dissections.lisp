#|
Copyright 2010 Carlo Hamalainen <carlo.hamalainen@gmail.com>. All 
rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions
are met:

   1. Redistributions of source code must retain the above copyright 
      notice, this list of conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright 
      notice, this list of conditions and the following disclaimer
      in the documentation and/or other materials provided with the
      distribution.

THIS SOFTWARE IS PROVIDED BY Carlo Hamalainen ``AS IS'' AND ANY EXPRESS
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL Carlo Hamalainen OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation 
are those of the authors and should not be interpreted as representing
official policies, either expressed or implied, of Carlo Hamalainen.
|#

; For debugging:
;(declaim (optimize (speed 0) (safety 3) (debug 3)))

; For computational runs:
(declaim (optimize (speed 3) (safety 0) (debug 0)))

; The element a + sqrt(3)*b in QQ(sqrt(3)) is represented by the 
; list (a b) where a and b are rationals.

(defun qq3prod (x y)
  "Product x*y where x, y are in QQ(sqrt(3))."
  (let* ((xa (first x))
	 (xb (second x))
	 (ya (first y))
	 (yb (second y)))
    (assert (= (length x) 2))
    (assert (= (length y) 2))

    ; calculating in Sage:
    ; var('xa'); var('xb'); var('ya'); var('yb');
    ; print ((xa + sqrt(3)*xb)*(ya + sqrt(3)*yb)).expand()
    ; sqrt(3)*xa*yb + sqrt(3)*xb*ya + xa*ya + 3*xb*yb
    ; which can be written as
    ; (xa*ya + 3*xb*yb) + (xa*yb + xb*y)*sqrt(3)
    (list (+ (* xa ya) (* 3 xb yb)) (+ (* xa yb) (* xb ya)))))

(defun qq3div-by-scalar (x y)
  "Computes x/y where x is in QQ(sqrt(3)) and y is an integer."
  (let ((xa (first x))
	(xb (second x)))
    (assert (= (length x) 2))
    (assert (integerp y))
    `(,(/ xa y) ,(/ xb y))))

(defun qq3add (x y)
  "Computes x + y where x, y are in QQ(sqrt(3))."
  (let ((xa (first x))
	(xb (second x))
	(ya (first y))
	(yb (second y)))
    (assert (= (length x) 2))
    (assert (= (length y) 2))
    (list (+ xa ya) (+ xb yb))))

(defun qq3sub (x y)
  "Computes x - y where x, y are in QQ(sqrt(3))."
  (let ((xa (first x))
	(xb (second x))
	(ya (first y))
	(yb (second y)))
    (assert (= (length x) 2))
    (assert (= (length y) 2))
    (list (- xa ya) (- xb yb)))) 

(assert (equal (qq3add '(1 1) '(3 4)) '(4 5)))
(assert (equal (qq3prod '(1 2) '(3 0)) '(3 6)))
(assert (equal (qq3prod '(1 2) '(0 3)) '(18 3)))
(assert (equal (qq3prod '(1 2) '(5 9)) '(59 19)))
 
(defun rotate-equilateral (x1 y1)
  "Suppose that the point (x1, y1) is in the unit equilateral triangle
with side along the x-axis from 0 to 1. This function rotates the point
x1,y1 about the centre of the equilateral triangle anticlockwise by angle 2*pi/3."
  (let ((x2 '(-1/2 0))   ; x2 = -1/2
	(y2 '(1/2 0)))   ; y2 = 1/2
    (setf x2 (qq3prod x2 '(0 1))) ; x2 *= sqrt(3)
    (setf x2 (qq3prod x2 y1))     ; x2 *= y1
    (setf x2 (qq3sub x2 (qq3prod '(1/2 0) x1)))
    (setf x2 (qq3add x2 '(1 0)))
    (setf y2 (qq3prod y2 '(0 1))) ; y2 *= sqrt(3)
    (setf y2 (qq3prod y2 x1))     ; y2 *= x1
    (setf y2 (qq3sub y2 (qq3prod '(1/2 0) y1)))
    (list x2 y2)))

(defun rotate-equilateral-inverse (x1 y1)
  "Inverse of ROTATE-EQUILATERAL."
  (let* ((rot1 (rotate-equilateral x1 y1))
	 (x2 (first rot1))
	 (y2 (second rot1)))
    (rotate-equilateral x2 y2)))

(assert (equal (rotate-equilateral '(0 0) '(0 0)) '((1 0) (0 0))))
(assert (equal (rotate-equilateral '(1 0) '(0 0)) '((1/2 0) (0 1/2))))
(assert (equal (rotate-equilateral '(1/2 0) '(0 1/2)) '((0 0) (0 0))))

(assert (equal (let ((rot1 (rotate-equilateral '(0 0) '(0 0))))
		 (rotate-equilateral-inverse (first rot1) (second rot1)))
	       '((0 0) (0 0))))

(defun reflect1 (x0 y)
  "Reflect along the line x = 1/2."
  (let ((x1 x0))
      (setf x1 (qq3sub x1 '(1/2 0)))
      (setf (first x1) (- (first x1)))
      (setf x1 (qq3add x1 '(1/2 0)))
      (list x1 y)))

(assert (equal (reflect1 '(1/4 0) '(0 0)) '((3/4 0) (0 0))))

(defun reflect2 (x1 y1)
  "The reflection of the equilateral triangle that fixes (0, 0)."
  (let* ((result1 (apply #'rotate-equilateral-inverse (list x1 y1)))
	 (result2 (apply #'reflect1 result1)))
    (apply #'rotate-equilateral result2)))

(assert (equal (reflect2 '(0 0) '(0 0)) '((0 0) (0 0))))
(assert (equal (reflect2 '(1 0) '(0 0)) '((1/2 0) (0 1/2))))

(defun reflect3 (x1 y1)
  "The reflection of the equilateral triangle that fixes (1, 0)."
  (let* ((result1 (apply #'rotate-equilateral (list x1 y1)))
	 (result2 (apply #'reflect1 result1)))
    (apply #'rotate-equilateral-inverse result2)))

(assert (equal (reflect3 '(1 0) '(0 0)) '((1 0) (0 0))))
(assert (equal (reflect3 '(0 0) '(0 0)) '((1/2 0) (0 1/2))))


(clc:clc-require 'split-sequence)

(defun split (string)
  "This is similar to Python's .split() function on strings."
  (split-sequence:split-sequence #\Space string :remove-empty-subseqs t))

(defun line-to-numbers (line)
  "Parse a string consisting of integers separated by spaces."
  (mapcar #'parse-integer (split line)))

(defun zero-list (n)
  (assert (> n 0))
  (loop repeat n collect 0))

; Corrected version of http://rosettacode.org/wiki/Reduced_row_echelon_form#Common_Lisp
; Only change is to the while loop of find-pivot:
(defun convert-to-row-echelon-form (matrix)
  (let* ((dimensions (array-dimensions matrix))
	 (row-count (first dimensions))
	 (column-count (second dimensions))
	 (lead 0))
    (labels ((find-pivot (start lead)
	       (let ((i start))
		 (loop 
		    :while (zerop (aref matrix i lead)) 
		    :do (progn
			  (incf i)
			  (when (= i row-count)
			    (setf i start)
			    (incf lead)
			    (when (= lead column-count)
			      (return-from convert-to-row-echelon-form matrix))))
		    :finally (return (values i lead)))))
	     (swap-rows (r1 r2)
	       (loop 
		  :for c :upfrom 0 :below column-count
		  :do (rotatef (aref matrix r1 c) (aref matrix r2 c))))
	     (divide-row (r value) 
	       (loop
		  :for c :upfrom 0 :below column-count
		  :do (setf (aref matrix r c)
			    (/ (aref matrix r c) value)))))
      (loop
	 :for r :upfrom 0 :below row-count
	 :when (<= column-count lead) 
	 :do (return matrix)
	 :do (multiple-value-bind (i nlead) (find-pivot r lead)
	       (setf lead nlead)
	       (swap-rows i r)
	       (divide-row r (aref matrix r lead))
	       (loop 
		  :for i :upfrom 0 :below row-count
		  :when (/= i r)
		  :do (let ((scale (aref matrix i lead)))
			(loop
			   :for c :upfrom 0 :below column-count
			   :do (decf (aref matrix i c)
				     (* scale (aref matrix r c))))))
	       (incf lead))
	 :finally (return matrix)))))


(defun identity-element-equations (identity-triple nr-rows nr-cols nr-syms)
  (multiple-value-bind (id-row id-col id-sym) (apply #'values identity-triple)
    (let ((m (+ nr-rows nr-cols nr-syms 1))
	  (row nil)
	  (equations nil))

      ; r_{id-row} = 0
      (setf row (zero-list m))
      (setf (nth id-row row) 1)
      (push row equations)

      ; c_{id-col} = 0
      (setf row (zero-list m))
      (setf (nth (+ id-col nr-rows) row) 1)
      (push row equations)

      ; s_{id-sym} = 1
      (setf row (zero-list m))
      (setf (nth (+ id-sym nr-rows nr-cols) row) 1)
      (setf (nth (- m 1) row) 1)
      (push row equations)

      equations)))

(defun normal-element-equations (triple nr-rows nr-cols nr-syms)
  (let ((r (first triple))
	    (c (second triple))
	    (s (third triple))
	    (m (+ nr-rows nr-cols nr-syms 1))
	    (row nil))

    ; r_{} + c_{} + s_{} = 0
    (setf row (zero-list m))
    (setf (nth r row) 1)                        ; new_row[r] = 1
    (setf (nth (+ c nr-rows) row) 1)            ; new_row[c + row_max] = 1
    (setf (nth (+ s nr-rows nr-cols) row) -1)   ; new_row[s + row_max+col_max] = -1
    row))

(defun equations-from-trade (trade identity-triple nr-rows nr-cols nr-syms)
  ; For full details on how these equations are constructed, see
  ; Drapal and Hamalainen, "An enumeration of equilateral triangle dissections", http://arxiv.org/abs/0910.5199
  (let ((equations nil))
    (loop for triple in trade
	 do (if (equal triple identity-triple)
		(setf equations (append equations (identity-element-equations identity-triple nr-rows nr-cols nr-syms)))
		(push (normal-element-equations triple nr-rows nr-cols nr-syms) equations)))
    equations))

(defun last-column (matrix)
  (let ((nr-rows (first (array-dimensions matrix)))
	(last-col (- (second (array-dimensions matrix)) 1)))
    (loop :for row :upfrom 0 :below nr-rows collect (aref matrix row last-col))))

(defun triangle-size (pt1 pt2 pt3)
  (let ((size nil))
    (when (equal (first pt1) (first pt2)) (setf size (abs (- (second pt1) (second pt2)))))
    (when (equal (second pt1) (second pt2)) (setf size (abs (- (first pt1) (first pt2)))))
    (when (null size) (setf size (triangle-size pt2 pt3 pt1)))
    size))

(assert (equal (triangle-size '(0 0) '(1 0) '(0 1)) 1))
(assert (equal (triangle-size '(1 0) '(0 1) '(0 0)) 1))
(assert (equal (triangle-size '(1 1) '(1 1) '(1 1)) 0))

(defun apply-transformation (fn points)
  (let ((image nil))
    (loop for xy in points do
	 (push (apply fn xy) image))
    image))

(defun point-to-4list (point)
  `(,@(first point) ,@(second point)))

(defun cmp-list< (x y)
  (let ((n (length x)))
    (assert (= (length x) (length y)))
    (loop :for i :upfrom 0 :below n do
       (when (< (nth i x) (nth i y)) (return-from cmp-list< t))
       (when (> (nth i x) (nth i y)) (return-from cmp-list< nil)))
    nil))

(defun cmp-list> (x y)
  (let ((n (length x)))
    (assert (= (length x) (length y)))
    (loop :for i :upfrom 0 :below n do
       (when (> (nth i x) (nth i y)) (return-from cmp-list> t))
       (when (< (nth i x) (nth i y)) (return-from cmp-list> nil)))
    nil))

(defun cmp-4list< (x y)
  (let ((n (length x)))
    (assert (= (length x) (length y)))
    (loop :for i :upfrom 0 :below n do
       (when (cmp-list< (nth i x) (nth i y)) (return-from cmp-4list< t))
       (when (cmp-list> (nth i x) (nth i y)) (return-from cmp-4list< nil)))
    nil))

(defun csig (points)
  (sort (mapcar #'point-to-4list points) #'cmp-list<))

(defun canonical-signature (points)
  (let (equilateral
	this-sig
	min-signature)
    (loop for xy in points do
	 (let* ((x (first xy))  ; should use multi-value bind?
		(y (second xy))
		(val-x (qq3add (qq3div-by-scalar y 2) x)) ; y/2 + x
		(val-y (qq3div-by-scalar (qq3prod '(0 1) y) 2))) ; sympy.sqrt(3)*y/2) 
	   (push `(,val-x ,val-y) equilateral)))

    ; Start off with the original image as having the minimum signature.
    (setf min-signature (csig equilateral))

    (loop for fn in '(reflect1 reflect2 reflect3 rotate-equilateral rotate-equilateral-inverse) do
	 (setf this-sig (csig (apply-transformation fn equilateral)))
	 ; (format t "this signature: ~a~%" this-sig)
	 (when (cmp-4list< this-sig min-signature) (setf min-signature this-sig)))

    min-signature))
    ; (format t "canonical signature: ~a~%~%" min-signature)))


(defun inject-into-qq3 (x)
  `(,x 0))


(defun is-separated-solution? (M nr-rows nr-cols nr-syms)
    (let* ((row-bits (remove-duplicates (subseq M 0 nr-rows)))
	   (col-bits (remove-duplicates (subseq M nr-rows (+ nr-rows nr-cols))))
	   (sym-bits (remove-duplicates (subseq M (+ nr-rows nr-cols)))))
      (and (= nr-rows (length row-bits))
	   (= nr-cols (length col-bits))
	   (= nr-syms (length sym-bits)))))

(defun solve-dissection-equations (nr-rows nr-cols nr-syms T1 T2 identity-triple-in-T1)
  (let* ((t-equations (equations-from-trade T1 identity-triple-in-T1 nr-rows nr-cols nr-syms))
	 (equations-as-array (make-array (list (length t-equations) (length (first t-equations))) :initial-contents t-equations))
	 (M (last-column (convert-to-row-echelon-form equations-as-array)))
	 (points nil))
    (if (not (is-separated-solution? M nr-rows nr-cols nr-syms)) (return-from solve-dissection-equations nil)
	(progn
	  (loop for triple in T2 do
	       (let* ((r (first triple))
		      (c (second triple))
		      (s (third triple))

		      (w1 (nth r M)) ; w1 = self.M[r]
		      (w2 (nth (+ c nr-rows) M)) ; w2 = self.M[c + self.row_max]
		      (w3 (nth (+ s nr-rows nr-cols) M)) ; w3 = self.M[s + self.row_max + self.col_max]

		      (pt1 (list w2 w1))         ; pt1 = (w2, w1)
		      (pt2 (list w2 (- w3 w2)))  ; pt2 = (w2, w3 - w2)
		      (pt3 (list (- w3 w1) w1)) ; pt3 = (w3 - w1, w1)

		      (fpt1 (mapcar #'inject-into-qq3 pt1))
		      (fpt2 (mapcar #'inject-into-qq3 pt2))
		      (fpt3 (mapcar #'inject-into-qq3 pt3)))

	         ; (format t "triangle: ~a has size ~a~%" `(,fpt1 ,fpt2 ,fpt3) (triangle-size fpt1 fpt2 fpt3))))

		 (push fpt1 points)
		 (push fpt2 points)
		 (push fpt3 points)))
	  (remove-duplicates points :test #'equal)))))

; This thing is a closure that pops out bitrades.
(defun bgen (spherical-bitrade-file)
  (let ((bitrade-file (open spherical-bitrade-file))
        header
	    nr-rows nr-cols nr-syms nr-cells
	    r c s rcs
	    T1 T2)
        #'(lambda ()
	    ; The first line has three numbers: the number of rows, 
	    ; columns, and symbols.
	    (setf header (read-line bitrade-file nil))

	    ; If we hit the end of the file we return nil, otherwise
	    ; we parse a complete bitrade and return the number of rows,
	    ; number of columns, number of symbols, and the bitrade itself.
	    (if (null header) nil
          (progn
	      (setf header (line-to-numbers header))
	      (setf nr-rows (first header))
	      (setf nr-cols (second header))
	      (setf nr-syms (third header))

  	      ; The next line has the number of cells in this trade.
	      (setf nr-cells (parse-integer (read-line bitrade-file nil)))

	      ; The next nr-cells rows have the trade T1.
	      (setf T1 nil)
	      (loop repeat nr-cells do
		   (setf rcs (line-to-numbers (read-line bitrade-file nil)))
		   (setf r (first rcs))
		   (setf c (second rcs))
		   (setf s (third rcs))
		   (setf T1 (append T1 `((,r ,c ,s)))))

              ; The next nr-cells rows have the trade T2.
	      (setf T2 nil)
	      (read-line bitrade-file nil) ; skip the number of elements of this trade
	      (loop repeat nr-cells do
		   (setf rcs (line-to-numbers (read-line bitrade-file nil)))
		   (setf r (first rcs))
		   (setf c (second rcs))
		   (setf s (third rcs))
		   (setf T2 (append T2 `((,r ,c ,s)))))

	    (list :nr-rows nr-rows :nr-cols nr-cols :nr-syms nr-syms :T1 T1 :T2 T2))))))

(defun enumerate-separated-dissections (min-size max-size)
  (loop :for i :upfrom min-size :upto max-size do
     (when (/= i 5)
       (with-open-file (out-file (concatenate 'string "separated_test_out_" (write-to-string i)) :direction :output :if-exists :supersede)
	 (format t "size = ~a~%" i)
	 (let* ((q (bgen (concatenate 'string "../spherical_bitrade_generator/spherical_bitrades_" (write-to-string i))))
		(result (funcall q))
		(nr-rows (getf result :nr-rows))
		(nr-cols (getf result :nr-cols))
		(nr-syms (getf result :nr-syms))
		(T1 (getf result :T1))
		(T2 (getf result :T2))
		(points nil))
	   (loop while (not (null result)) do
		; T1, T2
		(loop for identity-triple in T1 do
		     (setf points (solve-dissection-equations nr-rows nr-cols nr-syms T1 T2 identity-triple))
		     (when (= (+ i 2) (length points)) ; hmm
		       (setf *PRINT-PRETTY* nil)
		       (write-line (format nil "~a" (canonical-signature points)) out-file)
		       (setf *PRINT-PRETTY* t)))

	        ; T2, T1
		(loop for identity-triple in T2 do
		     (setf points (solve-dissection-equations nr-rows nr-cols nr-syms T2 T1 identity-triple))
		     (when (= (+ i 2) (length points)) ; only separated solutions
		       (setf *PRINT-PRETTY* nil)
		       (write-line (format nil "~a" (canonical-signature points)) out-file)
		       (setf *PRINT-PRETTY* t)))

                ; Move to the next one
		(setf result (funcall q))
		(setf nr-rows (getf result :nr-rows))
		(setf nr-cols (getf result :nr-cols))
		(setf nr-syms (getf result :nr-syms))
		(setf T1 (getf result :T1))
		(setf T2 (getf result :T2))))))))

