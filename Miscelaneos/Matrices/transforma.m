D= 			50;
L=			10;
Lambda = 	10;
lados = 	12;
vertices = 	8;

%-----------------------------------------------------
%	Coordenadas del modelo
%-----------------------------------------------------
%	Coordenadas de los vértices de un cubo de lado 2L en el espacio
%	a una distancia D del plano de proyección, usanso lente con distancia
%	focal L

p1= [-L,-L,D];
p2= [-L, L,D];
p3= [ L,-L,D];
p4= [ L, L,D];
p5= [-L,-L,D+L];
p6= [-L, L,D+L];
p7= [ L,-L,D+L];
p8= [ L, L,D+L];

Lista = [p1; p2; p3; p4; p5; p6; p7; p8];	% Lista de puntos  de vertices

%-----------------------------------------------------
%	Secuencia de pares de puntos para la generación de
% lineas -lados del cubo-

sec = [[1 2]; [1 3];[3 4];[2 4];[5 6];[5 7];[7 8];[6 8];[1 5];[2 6];[3 7];[4 8]];

%-----------------------------------------------------
%	Matrices  de transformación
%-----------------------------------------------------


%-----------------------------------------------------
% Traslación, matriz homogenea

Xo = 8;		%	Translada distancia en el eje  X
Yo = 5;		%	Translada distancia en el eje  Y
Zo = 0;		%	Translada distancia en el eje  Z

Tra = [	1 0 0 Xo;
		0 1 0 Yo;
		0 0 1 Zo;
		0 0 0  1];

%-----------------------------------------------------
% Escalado

Sx = 100;
Sy = 100;
Sz = 100;

Esc = [Sx  0  0  0;
		0 Sy  0  0;
		0  0 Sz  0;
		0  0  0  1];

%-----------------------------------------------------
% Rotacion un angulo  alrededor del eje Z

theta = 30;		%	Angulo de rotacion respecto al eje z
theta = theta*pi/180;

Roz = [	 cos(theta) sin(theta) 0  0;
		-sin(theta) cos(theta) 0  0;
		    0          0       1  0;
			0          0       0  1];

%-----------------------------------------------------
% Rotacion un angulo  alrededor del eje x

alfa = 30;		%	Angulo de rotacion respecto al eje x
alfa = alfa*pi/180;
Rox = [	1     0         0      0;
		0  cos(alfa) sin(alfa) 0;
		0 -sin(alfa) cos(alfa) 0;
		0     0         0      1];

%-----------------------------------------------------
% Rotacion un angulo  alrededor del eje y

beta = 45;		%	Angulo de rotacion respecto al eje y
beta = beta*pi/180;
Roy = [	cos(beta) 0 -sin(beta) 0;
		   0      1      0     0;
       	sin(beta) 0  cos(beta) 0;
		   0      0      0     1];

%-----------------------------------------------------
%	Transformacion en Perspectiva 
%	NOTA: 	
%		- 	Para un punto de coordenada en el espacio 
%			(X,Y,Z) al transformar en homogenea se debe multiplicar
%			por ubna constante K arbitraria: 

%			(	X, Y, Z, 1)*K = (KX, KY, KZ, K)

%		- 	Después de hacer las transformaciones correspondientes
%			el resultado es una coordenada homogenea. Para convertila 
%			a coordenada normal, se dividen las tres primeros elementos
%			entra el cuarto, pero como es una proyección al plano xy
%			la ccordenada z resultante no tiene significado, por lo que se
%			descarta
%				(xh,yh,zh, val) -> (xh,yh,zh)/val = (x,y,z) -> (x,y)

% 	Lambda = 

K = 1;

Per = [	1    0     0      0;
		0    1     0      0;
		0    0     1      0;
		0    0 -1/Lambda  1];

%------------------------------------------------
% Pruebas
%------------------------------------------------

%	Para todas las coordenadas de ls figura tridimensional

	%Ph = Esc*Ph; 		%	escala uniformmente 
	%Ph = Tra*Ph; 		%	traslada 2*L por el eje x 
	%Ph = Rox*Ph; 		%	Rota en torno a eje z
	

Ph = [Lista ones(8,1)];		%	Convertir lista de vèrtice en coordenadas homogeneasa
Ph = Ph'					%	Traspone para operar con matrices

%	Operaciones

%Ph = Esc*Ph 				%	Escala uniformmente 
%Ph = Tra*Ph 				%	Traslada 
Ph = Roz*Ph 				%	Rota en torno a eje z
Ph = Roy*Ph 				%	Rota en torno a eje y
Ph = Rox*Ph 				%	Rota en torno a eje x

%	Perspectiva

Po = Per*Ph					%	Se proyecta		
dosD = Po(1:2,:);			%	Extrae coordenadas x, y 
Div = Po(4,:);				%	Extrae cuarto vector para convertir homogenea a norma
Dn = [Div; Div];			%	Contruye matriz  duplicando vector
Pn= dosD./Dn;				%	Normaliza puntos x, y
Pn= Pn'						%	raspone para operar con matrices


%-----------------------------------------------------
%	Diagrama de la proyeccion

for i= 1:lados
	cx= [Pn(sec(i,1),1),Pn(sec(i,2),1)];
	cy= [Pn(sec(i,1),2),Pn(sec(i,2),2)];
	line(cx,cy)
end
axis([-30 30 -30 30])
grid
disp(['-------------------------------------'])
