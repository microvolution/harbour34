// Testing AltD() and Alert() coloring
// Notice you have to compile it using /b

PROCEDURE Main()

   AltD( 1 )   // Enables the debugger. Press <F5> to go

   Alert( "debugger enabled",, "GR+/B" )

   AltD()      // Invokes the debugger

   Alert( "debugger invoked",, "GR+" )

   Alert( "finished",, "GR+/B,W+/R" )  // 'W+/R' is ignored for Cl*pper compatibility and placed there for testing purposes only.

   RETURN
