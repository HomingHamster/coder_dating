from django.contrib.auth.models import User
from django.contrib.gis.db import models

languages = {
    "markup": "HTML & Markup",
    "css": "CSS",
    "clike": "C Like",
    "javascript": "JavaScript",
    "abap": "ABAP",
    "abnf": "ABNF",
    "actionscript": "ActionScript",
    "ada": "Ada",
    "agda": "Agda",
    "al": "AL",
    "antlr4": "ANTLR4",
    "apacheconf": "Apache Configuration",
    "apex": "Apex",
    "apl": "APL",
    "applescript": "AppleScript",
    "aql": "AQL",
    "arduino": "Arduino",
    "arff": "ARFF",
    "armasm": "ARM Assembly",
    "arturo": "Arturo",
    "asciidoc": "AsciiDoc",
    "aspnet": "ASP.NET(C#)",
    "asm6502": "6502 Assembly",
    "asmatmel": "Atmel AVR Assembly",
    "autohotkey": "AutoHotkey",
    "autoit": "AutoIt",
    "avisynth": "AviSynth",
    "avro-idl": "Avro IDL",
    "awk": "AWK",
    "bash": "Bash",
    "basic": "BASIC",
    "batch": "Batch",
    "bbcode": "BBcode",
    "bbj": "BBj",
    "bicep": "Bicep",
    "birb": "Birb",
    "bison": "Bison",
    "bnf": "BNF",
    "bqn": "BQN",
    "brainfuck": "Brainfuck",
    "brightscript": "BrightScript",
    "bro": "Bro",
    "bsl": "BSL (1C:Enterprise)",
    "c": "C",
    "csharp": "C#",
    "cpp": "C++",
    "cfscript": "CFScript",
    "chaiscript": "ChaiScript",
    "cil": "CIL",
    "cilkc": "Cilk/C",
    "cilkcpp": "Cilk/C++",
    "clojure": "Clojure",
    "cmake": "CMake",
    "cobol": "COBOL",
    "coffeescript": "CoffeeScript",
    "concurnas": "Concurnas",
    "csp": "Content-Security-Policy",
    "cooklang": "Cooklang",
    "coq": "Coq",
    "crystal": "Crystal",
    "css-extras": "CSS Extras",
    "csv": "CSV",
    "cue": "CUE",
    "cypher": "Cypher",
    "d": "D",
    "dart": "Dart",
    "dataweave": "DataWeave",
    "dax": "DAX",
    "dhall": "Dhall",
    "diff": "Diff",
    "django": "Django",
    "jinja2": "Jinja2",
    "dns-zone-file": "DNS Zone File",
    "docker": "Docker",
    "dot": "DOT (Graphviz)",
    "ebnf": "EBNF",
    "editorconfig": "EditorConfig",
    "eiffel": "Eiffel",
    "ejs": "EJS",
    "elixir": "Elixir",
    "elm": "Elm",
    "etlua": "Embedded Lua Templating",
    "erb": "ERB",
    "erlang": "Erlang",
    "excel-formula": "Excel Formula",
    "fsharp": "F#",
    "factor": "Factor",
    "false": "False",
    "firestore-security-rules": "Firestore Security Rules",
    "flow": "Flow",
    "fortran": "Fortran",
    "ftl": "FreeMarker Template Language",
    "gml": "GameMaker Language",
    "gap": "GAP (CAS)",
    "gcode": "G-code",
    "gdscript": "GDScript",
    "gedcom": "GEDCOM",
    "gettext": "gettext",
    "gherkin": "Gherkin",
    "git": "Git",
    "glsl": "GLSL",
    "gn": "GN",
    "linker-script": "GNU LinkerScript",
    "go": "Go",
    "go-module": "Go Module",
    "gradle": "Gradle",
    "graphql": "GraphQL",
    "groovy": "Groovy",
    "haml": "Haml",
    "handlebars": "Handlebars",
    "haskell": "Haskell",
    "haxe": "Haxe",
    "hcl": "HCL",
    "hlsl": "HLSL",
    "hoon": "Hoon",
    "http": "HTTP",
    "hpkp": "HTTP Public-Key-Pins",
    "hsts": "HTTP Strict-Transport-Security",
    "ichigojam": "IchigoJam",
    "icon": "Icon",
    "icu-message-format": "ICU Message Format",
    "idris": "Idris",
    "ignore": ".ignore",
    "inform7": "Inform7",
    "ini": "Ini",
    "io": "Io",
    "j": "J",
    "java": "Java",
    "javadoc": "JavaDoc",
    "javadoclike": "JavaDoc-like",
    "javastacktrace": "Java Stack Trace",
    "jexl": "Jexl",
    "jolie": "Jolie",
    "jq": "JQ",
    "jsdoc": "JSDoc",
    "js-extras": "JS Extras",
    "json": "JSON",
    "json5": "JSON5",
    "jsonp": "JSONP",
    "jsstacktrace": "JS Stack Trace",
    "js-templates": "JS Templates",
    "julia": "Julia",
    "keepalived": "Keepalived Configure",
    "keyman": "Keyman",
    "kotlin": "Kotlin",
    "kumir": "KuMir (КуМир)",
    "kusto": "Kusto",
    "latex": "LaTeX",
    "latte": "Latte",
    "less": "Less",
    "lilypond": "LilyPond",
    "liquid": "Liquid",
    "lisp": "Lisp",
    "livescript": "LiveScript",
    "llvm": "LLVM IR",
    "log": "Log File",
    "lolcode": "LOLCODE",
    "lua": "Lua",
    "magma": "Magma (CAS)",
    "makefile": "Makefile",
    "markdown": "Markdown",
    "markup-templating": "Markup Templating",
    "mata": "Mata",
    "matlab": "MATLAB",
    "maxscript": "MAXScript",
    "mel": "MEL",
    "mermaid": "Mermaid",
    "metafont": "METAFONT",
    "mizar": "Mizar",
    "mongodb": "MongoDB",
    "monkey": "Monkey",
    "moonscript": "MoonScript",
    "n1ql": "N1QL",
    "n4js": "N4JS",
    "nand2tetris-hdl": "Nand To Tetris HDL",
    "naniscript": "Naninovel Script",
    "nasm": "NASM",
    "neon": "NEON",
    "nevod": "Nevod",
    "nginx": "nginx",
    "nim": "Nim",
    "nix": "Nix",
    "nsis": "NSIS",
    "objectivec": "Objective-C",
    "ocaml": "OCaml",
    "odin": "Odin",
    "opencl": "OpenCL",
    "openqasm": "OpenQasm",
    "oz": "Oz",
    "parigp": "PARI / GP",
    "parser": "Parser",
    "pascal": "Pascal",
    "pascaligo": "Pascaligo",
    "psl": "PATROL Scripting Language",
    "pcaxis": "PC-Axis",
    "peoplecode": "PeopleCode",
    "perl": "Perl",
    "php": "PHP",
    "phpdoc": "PHPDoc",
    "php-extras": "PHP Extras",
    "plant-uml": "PlantUML",
    "plsql": "PL / SQL",
    "powerquery": "PowerQuery",
    "powershell": "PowerShell",
    "processing": "Processing",
    "prolog": "Prolog",
    "promql": "PromQL",
    "properties": ".properties",
    "protobuf": "Protocol Buffers",
    "pug": "Pug",
    "puppet": "Puppet",
    "pure": "Pure",
    "purebasic": "PureBasic",
    "purescript": "PureScript",
    "python": "Python",
    "qsharp": "Q#",
    "q": "Q (kdb + database)",
    "qml": "QML",
    "qore": "Qore",
    "r": "R",
    "racket": "Racket",
    "cshtml": "Razor C#",
    "jsx": "React JSX",
    "tsx": "React TSX",
    "reason": "Reason",
    "regex": "Regex",
    "rego": "Rego",
    "renpy": "Ren'py",
    "rescript": "ReScript",
    "rest": "reST (reStructuredText)",
    "rip": "Rip",
    "roboconf": "Roboconf",
    "robotframework": "RobotFramework",
    "ruby": "Ruby",
    "rust": "Rust",
    "sas": "SAS",
    "sass": "Sass (Sass)",
    "scss": "Sass (SCSS)",
    "scala": "Scala",
    "scheme": "Scheme",
    "shell-session": "Shell Session",
    "smali": "Smali",
    "smalltalk": "Smalltalk",
    "smarty": "Smarty",
    "sml": "SML",
    "solidity": "Solidity (Ethereum)",
    "solution-file": "Solution File",
    "soy": "Soy(Closure Template)",
    "sparql": "SPARQL",
    "splunk-spl": "Splunk SPL",
    "sqf": "SQFStatus Quo Function (Arma 3)",
    "sql": "SQL",
    "squirrel": "Squirrel",
    "stan": "Stan",
    "stata": "Stata Ado",
    "iecst": "Structured Text (IEC61131 3)",
    "stylus": "Stylus",
    "supercollider": "SuperCollider",
    "swift": "Swift",
    "systemd": "Systemd Configuration File",
    "t4-templating": "T4 Templating",
    "t4-cs": "T4 Text Templates(C#)",
    "t4-vb": "T4 Text Templates(VB)",
    "tap": "TAP",
    "tcl": "Tcl",
    "tt2": "Template Toolkit 2",
    "textile": "Textile",
    "toml": "TOML",
    "tremor": "Tremor",
    "turtle": "Turtle",
    "twig": "Twig",
    "typescript": "TypeScript",
    "typoscript": "TypoScript",
    "unrealscript": "UnrealScript",
    "uorazor": "UO Razor Script",
    "uri": "URI",
    "v": "V",
    "vala": "Vala",
    "vbnet": "VB.Net",
    "velocity": "Velocity",
    "verilog": "Verilog",
    "vhdl": "VHDL",
    "vim": "vim",
    "visual-basic": "Visual Basic",
    "warpscript": "WarpScript",
    "wasm": "WebAssembly",
    "web-idl": "Web IDL",
    "wgsl": "WGSL",
    "wiki": "Wiki Markup",
    "wolfram": "Wolfram Language",
    "wren": "Wren",
    "xeora": "Xeora",
    "xml-doc": "XML Doc(.net)",
    "xojo": "Xojo (REALbasic)",
    "xquery": "XQuery",
    "yaml": "YAML",
    "yang": "YANG",
    "zig": "Zig"
}

class CodeSnippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=31, choices=languages)
    date = models.DateField(auto_now_add=True)
    repository_url = models.CharField(max_length=200, blank=True, null=True)


class Opinion(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="opinion_by")
    on = models.ForeignKey(User, on_delete=models.CASCADE, related_name="opinion_on")
    opinion_type = models.CharField(max_length=1)


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.PointField()
    date = models.DateField(auto_now_add=True)


class Message(models.Model):
    message_text = models.TextField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
