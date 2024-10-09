import sys
sys.path.append('src/core/')
import data
from logic import EXPRESSION,OR,AND,TARGET,EQL,INCLUSION,MEMBERSHIP,COUNT,ALL,DATUM,EQL_GREATER
import time

# --------------------------------------------------------------------------------------
#                               ALPHABET/DICTIONARY
# --------------------------------------------------------------------------------------

# KEYWORD
KEYWORD_SET = {"SET","TUPLE","LIST","DICT","COUPLE",
               "NATURAL","INTEGER","RATIONAL","REAL","COMPLEX",
               "STRING","BOOL",'BINARY',"BYTE",
               "TRUE","FALSE","OR","AND","NOT",
               'FUNCTION','ACTION'}

# ALPHABET
LOWER_SET = { "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z" }
UPPER_SET = { "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z" } 
LETTER_SET = LOWER_SET.union(UPPER_SET)

# NUMERI
DIGIT_SET = {"0","1","2","3","4","5","6","7","8","9"}

# LEXICAL

# SYNTAX
CLOSURE_SET = { "\"","(",")","<",">","[","]","{","}","'", }
SEPARATOR_SET = { ",","|","::",":",";",'.','://',' ' }
SPECIAL_SET = {'\n','','\n\n','\\','_'}

SYMBOL_SET = { }

ARITHMETIC_SET = { "+","-","*","/","%" }
ASSIGNMENT_SET = { "=",":=","+=","-=","*=","/=","%=","^=","++","--" }
COMPARISON_SET = { "==","!=",">","<",">=","<=" }
LOGICAL_SET = { "&&","||","!",'?' }

OPERATOR_SET = LOGICAL_SET.union(ASSIGNMENT_SET,ARITHMETIC_SET,COMPARISON_SET)


# --------------------------------------------------------------------------------------
#                                LEXICAL
# --------------------------------------------------------------------------------------

OPERATOR = EXPRESSION('OPERATOR',MEMBERSHIP(TARGET,OPERATOR_SET))

KEYWORD = EXPRESSION('KEYWORD',MEMBERSHIP(TARGET,KEYWORD_SET))

ARITHMETIC = EXPRESSION('ARITHMETIC',MEMBERSHIP(TARGET,ARITHMETIC_SET))

SEPARATOR = EXPRESSION('SEPARATOR',MEMBERSHIP(TARGET,SEPARATOR_SET))

CLOSE = EXPRESSION('CLOSE',MEMBERSHIP(TARGET,CLOSURE_SET))

LETTER = EXPRESSION('LETTER',MEMBERSHIP(TARGET,LETTER_SET))

SPECIAL = EXPRESSION('SPECIAL',MEMBERSHIP(TARGET,SPECIAL_SET))

IDENTIFIER = EXPRESSION('IDENTIFIER',AND(
  MEMBERSHIP('@FirstChar',LETTER_SET),
  INCLUSION('@Stringa',LETTER_SET|DIGIT_SET),
),
  FirstChar=DATUM(data.Character,TARGET,data.ELEMENT,0),
  Stringa=DATUM(data.String,TARGET,data.NONE),
)

BOOLEAN = EXPRESSION('BOOLEAN',OR(
  EQL(TARGET,'True'),
  EQL(TARGET,'False'),
))

# NUMERI
BINARY = EXPRESSION('BINARY',INCLUSION(TARGET,{'0','1'}))
NATURAL = EXPRESSION('NATURAL',INCLUSION(TARGET,DIGIT_SET))
INTEGER = EXPRESSION('INTEGER',OR(
  NATURAL,
  AND(MEMBERSHIP('@FirstChar',DIGIT_SET|{'+','-'}),INCLUSION('@Digit',DIGIT_SET),COUNT('@Digit','',2,EQL_GREATER)),
),
  FirstChar=DATUM(data.Character,TARGET,data.ELEMENT,0),
  Digit=DATUM(data.String,TARGET,data.RANGE,1),
)
RATIONAL = EXPRESSION('INTEGER',AND(
  MEMBERSHIP('@FirstChar',DIGIT_SET|{'+','-'}),
  INCLUSION('@Digit',DIGIT_SET|{'.'}),
  OR(COUNT('@Digit','.',1),COUNT('@Digit','.',0)),
),
  FirstChar=DATUM(data.Character,TARGET,data.ELEMENT,0),
  Digit=DATUM(data.String,TARGET,data.RANGE,1),
)
REAL = EXPRESSION('INTEGER',AND(
  MEMBERSHIP('@FirstChar',DIGIT_SET|{'+','-','π','e'}),
  INCLUSION('@Digit',DIGIT_SET|{'.'}),
  OR(COUNT('@Digit','.',1),COUNT('@Digit','.',0)),
),
  FirstChar=DATUM(data.Character,TARGET,data.ELEMENT,0),
  Digit=DATUM(data.String,TARGET,data.RANGE,1),
)
#COMPLEX = EXPRESSION('BINARY',MEMBERSHIP(TARGET,['0','1']))

EMPTY = EXPRESSION('EMPTY',MEMBERSHIP(TARGET,set({None,'',0})))

NUMBER = EXPRESSION('NUMBER',OR(NATURAL,INTEGER,RATIONAL,BINARY))

STRING = EXPRESSION('STRING',AND(
  EQL('@TokenStart','"'),
  EQL('@TokenEnd','"'),
  COUNT(TARGET,'"',2),
),
  TokenStart=DATUM(data.Character,TARGET,data.ELEMENT,0),
  TokenEnd=DATUM(data.Character,TARGET,data.ELEMENT,-1),       
)

COMMENT = EXPRESSION('COMMENT',AND(
  EQL('@TokenStart','#'),
  EQL('@TokenEnd','\n'),
),
  TokenStart=DATUM(data.Character,TARGET,data.ELEMENT,0),
  TokenEnd=DATUM(data.Character,TARGET,data.ELEMENT,-1),       
)

CSTRING = EXPRESSION('CSTRING',AND(
  EQL('@TokenStart','"'),
  COUNT(TARGET,'"',1)
),
  TokenStart=DATUM(data.Character,TARGET,data.ELEMENT,0),
)
# --------------------------------------------------------------------------------------
#                                SYNTAX
# --------------------------------------------------------------------------------------


DATA_ALL = lambda worker,target,**kwargs: DATA(worker,target,**kwargs)

EXPRESSION_LINGUISTIC = EXPRESSION('LINGUISTIC',INCLUSION(TARGET,['0','1']))
EXPRESSION_LOGIC = EXPRESSION('LOGIC',INCLUSION(TARGET,['0','1']))
EXPRESSION_ALGEBRA = EXPRESSION('ALGEBRA',INCLUSION(TARGET,['0','1']))
EXPRESSION_ARITHMETIC = EXPRESSION('EXPRESSION_ARITHMETIC',AND(
  #INCLUSION(TARGET,['0','1'])
  ALL(TARGET,ARITHMETIC,NUMBER,IDENTIFIER),
  COUNT(TARGET,"",3,EQL_GREATER),
),
  #Nuovo=DATUM(data.Iterable,TARGET,data.PACK),
)

RECORD = EXPRESSION('RECORD',AND(
  EQL('@Primo','{'),
  OR(ALL('@Elementi',DATA_ALL),COUNT('@Mezzo',None,0)),
  EQL('@Ultimo','}'),
),
  Primo=DATUM(data.Character,TARGET,data.FIRST),
  Mezzo=DATUM(None,TARGET,data.RANGE,1,-1),
  Elementi=DATUM(data.Iterable,'@Mezzo',data.DIVISION,';'),
  Ultimo=DATUM(data.Character,TARGET,data.LAST),
)

# SET := '{' and '}' or ;
SET = EXPRESSION('SET',AND(
  EQL('@Primo','{'),
  OR(ALL('@Elementi',DATA_ALL),COUNT('@Mezzo',None,0)),
  EQL('@Ultimo','}'),
),
  Primo=DATUM(data.Character,TARGET,data.FIRST),
  Mezzo=DATUM(None,TARGET,data.RANGE,1,-1),
  Elementi=DATUM(data.Iterable,'@Mezzo',data.DIVISION,';'),
  Ultimo=DATUM(data.Character,TARGET,data.LAST),
)

TUPLE = EXPRESSION('TUPLE',AND(
  EQL('@Primo','('),
  #OR(ALL('@Elementi',DATA_ALL),COUNT('@Mezzo',None,0)),
  ALL('@Data',DATA_ALL),
  EQL('@Ultimo',')'),
),
  Primo=DATUM(data.Character,TARGET,data.FIRST),
  Mezzo=DATUM(None,TARGET,data.RANGE,1,-1),
  Data=DATUM(data.Iterable,'@Mezzo',data.DIVISION,','),
  Ultimo=DATUM(data.Character,TARGET,data.LAST),
)

AST = EXPRESSION('AST',AND(
  EQL('@Primo','('),
  #OR(ALL('@Elementi',DATA_ALL),COUNT('@Mezzo',None,0)),
  ALL('@Data',NUMBER,IDENTIFIER),
  EQL('@Ultimo',')'),
),
  Primo=DATUM(data.Character,TARGET,data.FIRST),
  Mezzo=DATUM(None,TARGET,data.RANGE,1,-1),
  Data=DATUM(data.Iterable,'@Mezzo',data.DIVISION,','),
  Ultimo=DATUM(data.Character,TARGET,data.LAST),
)
DATA_AST = lambda worker,target,**kwargs: AST(worker,target,**kwargs)

# PAIR := '(' ')' or :
PAIR = EXPRESSION('PAIR',AND(
  ALL('@Primo',NUMBER,IDENTIFIER,STRING),
  COUNT('@Pair',':',1),
  ALL('@Ultimo',NUMBER,IDENTIFIER,STRING),
),
  #Elementi=DATUM(data.Iterable,'@Pair',data.DIVISION,','),
  Primo=DATUM(None,'@Pair',data.FIRST),
  Ultimo=DATUM(None,'@Pair',data.LAST),
)
                    
# LIST := '[' ']' or ,
LIST = EXPRESSION('LIST',AND(
  EQL('@Primo','['),
  OR(ALL('@Elementi',DATA_ALL),COUNT('@Mezzo',None,0)),
  EQL('@Ultimo',']'),
),
  Primo=DATUM(data.Character,TARGET,data.FIRST),
  Mezzo=DATUM(None,TARGET,data.RANGE,1,-1),
  Data=DATUM(data.Iterable,'@Mezzo',data.DIVISION,','),
  Ultimo=DATUM(data.Character,TARGET,data.LAST),
)

# VECTOR := '[' ']' or ,
VECTOR = EXPRESSION('VECTOR',AND(
  EQL('@Primo','['),
  OR(ALL('@Elementi',DATA_ALL),COUNT('@Mezzo',None,0)),
  EQL('@Ultimo',']'),
),
  Primo=DATUM(data.Character,TARGET,data.FIRST),
  Mezzo=DATUM(None,TARGET,data.RANGE,1,-1),
  Elementi=DATUM(data.Iterable,'@Mezzo',data.DIVISION,','),
  Ultimo=DATUM(data.Character,TARGET,data.LAST),
)

# MATRIX := '[' ']' or ,
MATRIX = EXPRESSION('MATRIX',AND(
  EQL('@Primo','['),
  OR(ALL('@Data',DATA_ALL),COUNT('@Mezzo',None,0)),
  EQL('@Ultimo',']'),
),
  Primo=DATUM(data.Character,TARGET,data.FIRST),
  Mezzo=DATUM(None,TARGET,data.RANGE,1,-1),
  Data=DATUM(data.Iterable,'@Mezzo',data.DIVISION,','),
  Ultimo=DATUM(data.Character,TARGET,data.LAST),
)

# DICTIONARY := '{' ... PAIR ... '}' or ;
DICTIONARY = EXPRESSION('DICTIONARY',AND(
  EQL('@Primo','{'),
  #ANY(['@Elementi',"100"],[PAIR]),
  ALL('@Elementi',[PAIR]),
  #EACH(ANY,[PAIR],['@Elementi']),
  EQL('@Ultimo','}'),
),
  Primo=DATUM(data.Character,TARGET,data.FIRST),
  Mezzo=DATUM(data.Iterable,TARGET,data.RANGE,1,-1),
  Elementi=DATUM(data.Iterable,'@Mezzo',data.DIVISION,';'),
  Ultimo=DATUM(data.Character,TARGET,data.LAST),
)

# FN:varname := (STRING:a){ return a }(a)
FUNCTION = EXPRESSION('FUNCTION',AND(
  ALL(TARGET,TUPLE),
  ALL(TARGET,SET),
  ALL(TARGET,TUPLE),
),
  Primo=DATUM(data.Character,TARGET,data.FIRST),
  Mezzo=DATUM(data.Iterable,TARGET,data.RANGE,1,-1),
  Elementi=DATUM(data.Iterable,'@Mezzo',data.DIVISION,';'),
  Ultimo=DATUM(data.Character,TARGET,data.LAST),
)

# OBJECT := []KEYWORD:IDENTIFIER
OBJECT = EXPRESSION('OBJECT',MEMBERSHIP(TARGET,['0','1']))
# TREE := 2 | 2 / 1 | 2 -> 0  1 / 1:0 | 1 -> 0
TREE = EXPRESSION('TREE',MEMBERSHIP(TARGET,['0','1']))
# GRAPH := A:B,C,D|B:C|C:D|D:A
GRAPH = EXPRESSION('GRAPH',MEMBERSHIP(TARGET,['0','1']))
# STACK := <0-1-2-3-4-5-6-7-8-9>
STACK = EXPRESSION('STACK',MEMBERSHIP(TARGET,['0','1']))
# QUEUE := <9-8-7-6-5-4-3-2-1-0>
QUEUE = EXPRESSION('QUEUE',MEMBERSHIP(TARGET,['0','1']))

# ALL DATA
# NUMBER,STRING,BOOLEAN,IDENTIFIER,TUPLE STRING,NUMBER,BOOLEAN,
DATA = EXPRESSION('DATA',AND(
  #ANY('@Token',[IDENTIFIER,STRING,NUMBER]),
  OR(ALL('@Token',IDENTIFIER,STRING,NUMBER),ALL('@Data',EXPRESSION_ARITHMETIC,STRING)),
  #ALL('@Un',EXPRESSION_ARITHMETIC),
  #COUNT('@Token','',1,EQL_GREATER),
),
  Token=DATUM(data.String,'@Data',data.UNPACK),
  Un=DATUM(data.Iterable,'@Data',data.PACK),
)

INSTRUCTION_CALL = EXPRESSION('CALL',AND(
  ALL('@Primo',[IDENTIFIER]),
  ALL('@Tuple',[TUPLE]),
),
  Primo=DATUM(data.String,TARGET,data.FIRST),
  Tuple=DATUM(data.Iterable,TARGET,data.RANGE,1),
)

#INSTRUCTION_ALLOCATION = KEYWORD:IDENTIFIER := DATA
INSTRUCTION_ALLOCATION = EXPRESSION('ALLOCATION', AND(
  ALL('@Pair',PAIR),
  EQL(':=','@Operator'),
  ALL('@Data',DATA),
),
  Pair=DATUM(data.Iterable,TARGET,data.RANGE,0,3),
  Operator=DATUM(data.String,TARGET,data.ELEMENT,3),
  Data=DATUM(data.Iterable,TARGET,data.RANGE,4),
)

# DEAL id
INSTRUCTION_DEALLOCATE = EXPRESSION('DEALLOCATE', AND(
  EQL('DEAL','_0'),
  DATA,
),
  Id=DATUM(None,TARGET,data.ELEMENT,0),
  Operator=DATUM(None,TARGET,data.ELEMENT,1),
  Data=DATUM(data.Iterable,TARGET,data.RANGE,4),
)

# varname = data
INSTRUCTION_ASSIGNMENT = EXPRESSION('ASSIGNMENT', AND(
  ALL('@Id',IDENTIFIER),
  EQL('=',"@Operator"),
  ALL('@Data',[DATA]),
),
  Id=DATUM(None,TARGET,data.ELEMENT,0),
  Operator=DATUM(data.Character,TARGET,data.ELEMENT,1),
  Data=DATUM(data.Iterable,TARGET,data.RANGE,2),
)

INSTRUCTION_JOB = EXPRESSION('JOB',MEMBERSHIP(TARGET,['0','1']))
INSTRUCTION_SYSTEM = EXPRESSION('SYSTEM',MEMBERSHIP(TARGET,['0','1']))
INSTRUCTION_INPUT = EXPRESSION('INPUT',MEMBERSHIP(TARGET,['0','1']))
INSTRUCTION_OUTPUT = EXPRESSION('OUTPUT',MEMBERSHIP(TARGET,['0','1']))
INSTRUCTION_RETURN = EXPRESSION('RETURN',AND(EQL('RETURN',TARGET),DATA))
INSTRUCTION_WAIT = EXPRESSION('WAIT',MEMBERSHIP(TARGET,['0','1']))
INSTRUCTION_NEXT = EXPRESSION('NEXT',MEMBERSHIP(TARGET,['0','1']))
INSTRUCTION_LOCK = EXPRESSION('LOCK',MEMBERSHIP(TARGET,['0','1']))

INSTRUCTION_COMPARISON = EXPRESSION('JOB',MEMBERSHIP(TARGET,['0','1']))
INSTRUCTION_CONVERSION = EXPRESSION('CONVERSION',MEMBERSHIP(TARGET,['0','1']))
INSTRUCTION_CONCATENATION = EXPRESSION('CONCATENATION',MEMBERSHIP(TARGET,['0','1']))
INSTRUCTION_ITERATION = EXPRESSION('ITERATION',MEMBERSHIP(TARGET,['0','1']))
INSTRUCTION_INCREASE_DECREASE = EXPRESSION('JOB',MEMBERSHIP(TARGET,['0','1']))
INSTRUCTION_SELECTION = EXPRESSION('SELECTION',MEMBERSHIP(TARGET,['0','1']))
INSTRUCTION_LOGICAL = EXPRESSION('LOGICAL',MEMBERSHIP(TARGET,['0','1']))
INSTRUCTION_ARITHMETIC = EXPRESSION('ARITHMETIC',MEMBERSHIP(TARGET,['0','1']))
INSTRUCTION_ALGEBRAIC = EXPRESSION('ALGEBRAIC',MEMBERSHIP(TARGET,['0','1']))

INSTRUCTION_BLOCK = EXPRESSION('BLOCK',AND(
  EQL('@Primo','{'),
  OR(ALL('@Elementi',[INSTRUCTION_ALLOCATION,INSTRUCTION_ASSIGNMENT,INSTRUCTION_CALL],True),COUNT('@Mezzo',None,1)),
  EQL('@Ultimo','}'),
),
  Primo=DATUM(data.Character,TARGET,data.FIRST),
  Ultimo=DATUM(data.Character,TARGET,data.LAST),
  Mezzo=DATUM(None,TARGET,data.RANGE,1,-1),
  Elementi=DATUM(data.Iterable,'@Mezzo',data.DIVISION,';'),
  
)