// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

@1
D=M
@times
M=D // copy R1 into D and set M to R1 for @times

@2
M=0 // initialize answer to 0


(LOOP)
  @times
  D=M
  @END
  D; JEQ // end loop if times=0

  @1
  D=D-A
  @times
  M=D // update times

  @2
  D=M
  @0
  D=D+M
  @2
  M=D // add one R0 val to sum

  @LOOP
  0; JMP
(END)
@END
0; JMP
