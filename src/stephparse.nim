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


proc TokenStream(input): tuple =
  var 
    current = Null
    keywords = " if then else lambda λ true false "
    result = tuple[next: char, peek: char, eof: bool, croak: bool]

  return

  proc is_keyword(x): bool =
    return keywords.indexOf(" " + x + " ") >= 0

  proc is_digit(ch: char): bool =
    return (ch in Digits)

  proc is_id_start(ch: char): bool =
    return (ch in Letters)

  proc is_id(ch: char): bool =
    return (is_id_start(ch) || ch in "?!-<>=0123456789")

  proc is_op_char(ch: char): bool =
    return (ch in "+-*/%=&|<>!")

  proc is_punc(ch: char): bool =
    return (ch in ",;(){}[]")

  proc is_whitespace(ch: char): bool =
    return (ch in Whitespace)

  proc read_while(predicate): string =
    var str = ""
    while (!input.eof() && predicate(input.peek())):
      str += input.next()
    return str

  proc read_number(): tuple =
    var
      has_dot = false
      number = read_while(function(ch))
      result = tuple[typee: string, value: float]

    result.typee = "num"
    result.value = parseFloat(number)
    return

    proc function(ch): bool =
      if (ch == "."):
        if (has_dot):
          return false
        has_dot = true
        return true
      return is_digit(ch)

  proc read_ident():

    function read_ident() {
        var id = read_while(is_id);
        return {
            type  : is_keyword(id) ? "kw" : "var",
            value : id
        };
    }

    function read_escaped(end) {
        var escaped = false, str = "";
        input.next();
        while (!input.eof()) {
            var ch = input.next();
            if (escaped) {
                str += ch;
                escaped = false;
            } else if (ch == "\\") {
                escaped = true;
            } else if (ch == end) {
                break;
            } else {
                str += ch;
            }
        }
        return str;
    }

    function read_string() {
        return { type: "str", value: read_escaped('"') };
    }

    function skip_comment() {
        read_while(function(ch){ return ch != "\n" });
        input.next();
    }

    function read_next() {
        read_while(is_whitespace);
        if (input.eof()) return null;
        var ch = input.peek();
        if (ch == "#") {
            skip_comment();
            return read_next();
        }
        if (ch == '"') return read_string();
        if (is_digit(ch)) return read_number();
        if (is_id_start(ch)) return read_ident();
        if (is_punc(ch)) return {
            type  : "punc",
            value : input.next()
        };
        if (is_op_char(ch)) return {
            type  : "op",
            value : read_while(is_op_char)
        };
        input.croak("Can't handle character: " + ch);
    }

    function peek() {
        return current || (current = read_next());
    }

    function next() {
        var tok = current;
        current = null;
        return tok || read_next();
    }

    function eof() {
        return peek() == null;
    }
}

TokenStream(InputStream("testing"))
