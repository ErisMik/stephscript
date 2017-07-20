import strutils

proc InputStream(input: string): tuple =
  var 
    pos, col = 0
    line = 1
    result: tuple[next: char, peek: char, eof: bool, croak: bool]

  proc next(): char =
    var ch = input[pos]
    pos = pos + 1
    if (ch in  strutils.NewLines):
      line = line + 1
      col = 0
    else:
      col = col + 1
    return ch

  proc peek(): char =
    return input[pos]

  proc eof(): bool =
    return peek() == '~'

  proc croak(): bool =
    return false

  result.next = next()
  result.peek = peek()
  result.eof = eof()
  result.croak = croak()
  return

InputStream("testing")
