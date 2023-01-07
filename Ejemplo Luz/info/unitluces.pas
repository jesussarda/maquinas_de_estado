//-----------------------------------------------------
//  Problema: Control de la luz de un pasillo público
//-----------------------------------------------------
//  - El pasillo dispone de dos pulsadores, uno al lado de cada puerta, de
//  manera que se pueda encender y apagar la luz desde cada extremo. Cada
//  pulsador produce un ‘1’ lógico mientras está pulsado, y un ‘0’ lógico
//  cuando no lo está.
//  - Se desea que, cada vez que se pulse cualquier pulsador, la luz cambie
//  de estado: si está apagada se debe encender, y viceversa.
//  - Se debe tener en cuenta el caso en el que, mientras se pulsa un
//  interruptor, se pulse el otro. Por ejemplo, si estando apagada la luz,
//  alguien pulsa P1 se enciende la luz. Pero si mientras está pulsado P1
//  alguien pulsa P2, entonces se apagará nuevamente la luz.
//  - Hay que considerar la simultaneidad de pulsaciones

unit UnitLuces;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, FileUtil, Forms, Controls, Graphics, Dialogs, ExtCtrls,
  StdCtrls, UnitMatriz, UnitGlobal;

type

  { TfrmLuces }

  TfrmLuces = class(TForm)
    btnSwitchP1: TButton;
    btnSwitchP2: TButton;
    btnSalir: TButton;
    shpLuz: TShape;
    shpTecho: TShape;
    procedure btnSalirClick(Sender: TObject);
    procedure btnSwitchP2Click(Sender: TObject);
    procedure btnSwitchP1Click(Sender: TObject);
    procedure FormActivate(Sender: TObject);
  private
    { private declarations }
  public
    { public declarations }
  end;

var
  frmLuces: TfrmLuces;

  Maquina:    CMatrizEdo;
  iEve:       integer;
  Accion:     RSalida;
  //MatrizDeTransiciones: MatrizE;

  Sw:   Sws;
  dato: Integer;
  i:    Integer;

  //------------------------------------------------------
  //  Prototipo de funciones

  function    LeeEventos(var sens: Sws): integer;
  function    SalidaAccion(Indice: integer): RSalida;


implementation

{$R *.lfm}

{ TfrmLuces }

//--------------------------------------------------------
// Función Global de conversion.
// --------------------------------------------------------
//    Convierte una cantidad de variables booleanas
//    en un su representacion entera

//    NOTA: Hasta 16 0 32 variables o sensores
//          dependiendo de definición de integer

function LeeEventos(var sens: Sws): integer;
    var
       mask: integer;
       dato: integer;
       i:    integer;

    begin
        mask:=  1;
        dato:=  0;
        for i:= 0 to NumEventos-1 do
            if sens[i] then
                dato:= dato OR (mask shl i);
        LeeEventos:= dato and MaskSens;
    end;

//--------------------------------------------------------
//  Función o conjunto de funciones de salida. Tantas como
//  acciones esten declaradas
//  (Dependientes del problema)
// --------------------------------------------------------


function SalidaAccion(Indice: integer): RSalida;
    var
        Sale:  RSalida;

    begin
      case Indice of

        //---------------------------------------------
        //  Se apaga la luz
        0:  Begin
                frmLuces.shpLuz.Brush.Color:= clBlack;
                frmLuces.shpTecho.Brush.Color:= clBlack;
            end

        //---------------------------------------------
        //  Se enciende la luz
        else
            begin
                frmLuces.shpLuz.Brush.Color:= clwhite;
                frmLuces.shpTecho.Brush.Color:= clGray;
            end;
      end;

        SalidaAccion:= Sale;
    end;


//-------------------------------------------------------
//  ACTIVACION del simulador

procedure TfrmLuces.FormActivate(Sender: TObject);
  begin
    //--------------------------------
    //  Inicializa vector de eventos

    for i:= 0 to NumEventos-1 do
        Sw[i]:= false;


    //--------------------------------------------
    // Creación y configuración de la Máquina

    Maquina:=  CMatrizEdo.Crear(NumEstados,NumEventos,NumAcciones);

    //----------------------------------------------
    //  Estados según grafo

    Maquina.AgregaEstado('S0');	    // Indice 0
    Maquina.AgregaEstado('S1');	    // Indice 1
    Maquina.AgregaEstado('S2');	    // Indice 2
    Maquina.AgregaEstado('S3');	    // Indice 3
    Maquina.AgregaEstado('S4');	    // Indice 4
    Maquina.AgregaEstado('S5');	    // Indice 5

    //----------------------------------------------
    //  Eventos:

    Maquina.AgregaEvento('00');	// Indice 0
    Maquina.AgregaEvento('01');	// Indice 1
    Maquina.AgregaEvento('10');	// Indice 2
    Maquina.AgregaEvento('11');	// Indice 3

    //----------------------------------------------
    //  Acciones:

    Maquina.AgregaAccion('apaga',   @SalidaAccion);	 // Indice 0
    Maquina.AgregaAccion('prende',  @SalidaAccion);	 // Indice 1


    //----------------------------------------------
    //   Tabla de transisiones y acciones según grafo

    //  Estado S0
    Maquina.AgregaTransicion('S0','00', 'S0', 'apaga');   // Espera por monedas
    Maquina.AgregaTransicion('S0','01', 'S1', 'apaga');   // Espera por monedas
    Maquina.AgregaTransicion('S0','10', 'S1', 'apaga');   // Espera por monedas
    Maquina.AgregaTransicion('S0','11', 'S0', 'apaga');   // Espera por monedas

    //  Estado S1
    Maquina.AgregaTransicion('S1','00', 'S3', 'prende');   // Espera por monedas
    Maquina.AgregaTransicion('S1','01', 'S1', 'prende');   // Espera por monedas
    Maquina.AgregaTransicion('S1','10', 'S1', 'prende');   // Espera por monedas
    Maquina.AgregaTransicion('S1','11', 'S2', 'prende');   // Espera por monedas

    //  Estado S2
    Maquina.AgregaTransicion('S2','00', 'S2', 'apaga');   // Espera por monedas
    Maquina.AgregaTransicion('S2','01', 'S4', 'apaga');   // Espera por monedas
    Maquina.AgregaTransicion('S2','10', 'S4', 'apaga');   // Espera por monedas
    Maquina.AgregaTransicion('S2','11', 'S2', 'apaga');   // Espera por monedas

    //  Estado S3
    Maquina.AgregaTransicion('S3','00', 'S3', 'prende');   // Espera por monedas
    Maquina.AgregaTransicion('S3','01', 'S4', 'prende');   // Espera por monedas
    Maquina.AgregaTransicion('S3','10', 'S4', 'prende');   // Espera por monedas
    Maquina.AgregaTransicion('S3','11', 'S3', 'prende');   // Espera por monedas

    //  Estado S4
    Maquina.AgregaTransicion('S4','00', 'S0', 'apaga');   // Espera por monedas
    Maquina.AgregaTransicion('S4','01', 'S4', 'apaga');   // Espera por monedas
    Maquina.AgregaTransicion('S4','10', 'S4', 'apaga');   // Espera por monedas
    Maquina.AgregaTransicion('S4','11', 'S5', 'apaga');   // Espera por monedas

    //  Estado S5
    Maquina.AgregaTransicion('S5','00', 'S5', 'prende');   // Espera por monedas
    Maquina.AgregaTransicion('S5','01', 'S1', 'prende');   // Espera por monedas
    Maquina.AgregaTransicion('S5','10', 'S1', 'prende');   // Espera por monedas
    Maquina.AgregaTransicion('S5','11', 'S5', 'prende');   // Espera por monedas

    //----------------------------------------------
    //   Establecer Estado inicial segun grafo

    Maquina.EstadoInicial('S0');


    //---------------------------------------------
    // Inicializaciones de la Simulación

    shpLuz.Brush.Color:= clBlack;
    shpTecho.Brush.Color:= clBlack;


  end;

//-------------------------------------------------------
// BOTON: Salir
//-------------------------------------------------------

procedure TfrmLuces.btnSalirClick(Sender: TObject);
  begin
        frmLuces.Close;
  end;


//-------------------------------------------------------
// BOTON: P1 (Puerta 1)
//-------------------------------------------------------

procedure TfrmLuces.btnSwitchP1Click(Sender: TObject);
  begin

    Sw[0]:= not Sw[0];

    iEve:=  LeeEventos(Sw);                 // Codifica eventos
    Accion:= Maquina.HacerTransicion(iEve); // Ejecuta acción
    //lblSurtidor.Caption:= Accion.Mensaje;
    //SalidaAccion(iEve);

{    if not Sw[0] then
        begin
          //shpLuz.Brush.Color:= clWhite;
          //shpTecho.Brush.Color:= clGray;
        end
    else
        begin
          //shpLuz.Brush.Color:= clBlack;
          //shpTecho.Brush.Color:= clBlack;
        end; }

  end;


//-------------------------------------------------------
// BOTON: P1 (Puerta 1)
//-------------------------------------------------------

procedure TfrmLuces.btnSwitchP2Click(Sender: TObject);
  begin

    Sw[1]:= not Sw[1];

    iEve:=  LeeEventos(Sw);                 // Codifica eventos
    Accion:= Maquina.HacerTransicion(iEve); // Ejecuta acción
    //lblSurtidor.Caption:= Accion.Mensaje;
    //    SalidaAccion(iEve);
{     if not Sw[1] then
         begin
           //shpLuz.Brush.Color:= clWhite;
           //shpTecho.Brush.Color:= clGray;
         end
     else
         begin
           //shpLuz.Brush.Color:= clBlack;
           //shpTecho.Brush.Color:= clBlack;
         end;
         }
  end;

end.

