verbatimtex
\documentclass[12pt]{article}

%\usepackage[mathlf,minionint]{MinionPro} \usepackage[T1]{fontenc} \usepackage{textcomp}
\usepackage{amssymb}

\begin{document}
etex

def whiteCircle(expr p, b) =
begingroup
	fill fullcircle scaled b shifted p withcolor white;
	draw fullcircle scaled b shifted p;
endgroup
enddef;

def blackCircle(expr p, b) =
begingroup
	draw p withpen pencircle scaled b;
endgroup
enddef;

vardef TEX primary s =
   write "verbatimtex"                    to "mptextmp.mp";
   write "\documentclass[12pt]{article}"  to "mptextmp.mp";
   %write "\usepackage[T1]{fontenc}"       to "mptextmp.mp";
   %write "\usepackage{amsmath,amssymb}"   to "mptextmp.mp";
   write "\begin{document}"               to "mptextmp.mp";
   write "etex"                           to "mptextmp.mp";
   write "btex "&s&" etex"                to "mptextmp.mp";
   write EOF                              to "mptextmp.mp";
   scantokens "input mptextmp"
enddef;


	% Makes arrow heads go half way.
	save arrowhead;
	vardef arrowhead expr p =
		save A,u; pair A,u;
		A := point 1/2length(p) of p;
		u := unitvector(direction 1/2length(p) of p);
		A -- (A - ahlength*u rotated 25) --
		(A - ahlength*u rotated -25) -- cycle
	enddef;

beginfig(1)
	u := 2cm;

	pair X,A,B;

	X := (0,0);
	A := u * dir 0;
	B := u * dir 60;

	blackCircle(X, 4bp);
	blackCircle(A, 4bp);
	blackCircle(B, 4bp);

	drawarrow X -- A;
	drawarrow A -- B;
	drawarrow B -- X;

	label.urt(btex $\circlearrowleft$ etex, 1/2[X, 1/2[A,B]]);

	label.rt(btex $x = x \tau_1 \tau_2 \tau_3$ etex, A);
	label.top(btex $x \tau_1$ etex, B);
	label.lft(btex $x \tau_1 \tau_2$ etex, X);


	pair x;

	x := (4u, 0) + (0, ypart(1/2[X, 1/2[A,B]]));

	blackCircle(u*dir(0*360/6) + x, 4bp);
	blackCircle(u*dir(1*360/6) + x, 4bp);
	blackCircle(u*dir(2*360/6) + x, 4bp);
	blackCircle(u*dir(3*360/6) + x, 4bp);
	blackCircle(u*dir(4*360/6) + x, 4bp);
	blackCircle(u*dir(5*360/6) + x, 4bp);

	drawarrow (u*dir(0*360/6) + x) -- (u*dir(1*360/6) + x);
	drawarrow (u*dir(1*360/6) + x) -- (u*dir(2*360/6) + x);
	drawarrow (u*dir(2*360/6) + x) -- (u*dir(3*360/6) + x);
	drawarrow (u*dir(3*360/6) + x) -- (u*dir(4*360/6) + x);
	drawarrow (u*dir(4*360/6) + x) -- (u*dir(5*360/6) + x);
	drawarrow (u*dir(5*360/6) + x) -- (u*dir(0*360/6) + x);

	% In Minion Pro, \circlearrowright produced a left arrow,
	% yet the 'l' prefix fixes it up!? So bizzare.
	%label(btex $\lcirclearrowright$ etex, x);
	label(btex $\circlearrowright$ etex, x);

	label.rt( btex $x = x \tau_1^6$ etex, u*dir(0*360/6) + x);
	label.top(btex $x \tau_1$ etex, u*dir(1*360/6) + x);
	label.top(btex $x \tau_1^2$ etex, u*dir(2*360/6) + x);
	label.lft(btex $x \tau_1^3$ etex, u*dir(3*360/6) + x);
	label.bot(btex $x \tau_1^4$ etex, u*dir(4*360/6) + x);
	label.bot(btex $x \tau_1^5$ etex, u*dir(5*360/6) + x);

endfig;

beginfig(2)
	u := 2cm;

	pair X,A,B,C,D,E,F;

	X := (0,0);
	A := u * dir 0;
	B := u * dir 60;
	C := u * dir 120;
	D := u * dir 180;
	E := u * dir 240;
	F := u * dir 300;

	pickup pencircle scaled 4pt;
	draw X;
	draw A;
	draw B;
	draw C;
	draw D;
	draw E;
	draw F;

	pickup defaultpen;

	draw X--A;
	draw X--B;
	draw X--C;
	draw X--D;
	draw X--E;
	draw X--F;

	draw A--B;
	drawarrow A -- B;

	draw C--D;
	drawarrow C-- D;

	draw E--F;
	drawarrow E-- F;
	
	drawarrow origin -- A;
	drawarrow B -- origin;
	drawarrow origin -- C;
	drawarrow D -- origin;
	drawarrow origin -- E;
	drawarrow F -- origin;

	label.urt(btex $t_1$ etex, 1/2[X, 1/2[A,B]]);
	label.ulft(btex $t_2$ etex, 1/2[X, 1/2[C,D]]);
	label.bot(btex $t_3$ etex, 1/2[X, 1/2[E,F]]);

	label.rt(btex $x \tau_2$ etex, A);
	label.top(btex $x \tau^{-1}_3$ etex, B);
	label.top(btex $x \tau_3$ etex, C);
	label.lft(btex $x \tau^{-1}_1$ etex, D);
	label.bot(btex $x \tau_1$ etex, E);
	label.bot(btex $x \tau^{-1}_2$ etex, F);

	% New part is here.
	drawarrow A .. F dashed evenly;
	label.lrt(btex $\mu_2$ etex, 1/2[X, 1/2[A,F]]);
	
	drawarrow E .. D dashed evenly;
	label.llft(btex $\mu_1$ etex, 1/2[X, 1/2[E,D]]);
	
	drawarrow C .. B dashed evenly;
	label.top(btex $\mu_3$ etex, 1/2[X, 1/2[C,B]]);
endfig;

end
