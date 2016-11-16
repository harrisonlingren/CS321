// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

@SCREEN
D=A
@screen_pos
M=D // set screen_pos to SCREEN

@8191
D=A
@SCREEN
D=D+A
@screen_max
M=D // set screen size

(START)
  @KBD
  D=M
  @BLANK
  D; JEQ // if no key pressed, blank screen

  @FILL
  0;JMP // else, fill

(FILL)
  @screen_pos
  A=M
  M=-1
  @UPDATE
  0; JMP // fill one pixel

(BLANK)
  @screen_pos
  A=M
  M=0
  @UPDATE
  0; JMP // clear one pixel

(UPDATE)
  @screen_pos
  D=M+1
  M=D // add one to position

  @screen_max
  D=D-M
  @START
  D; JNE // Set D to screen_pos - screen_max, reset if not ==

  @SCREEN
  D=A
  @screen_pos
  M=D
  @START
  0; JMP // else, reset M
