; ModuleID = "meu_modulo.bc"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"a" = common global i32 0, align 4
define i32 @"main"() 
{
inicio_main:
  %"ret" = alloca i32
  %"b" = alloca i32, align 4
  store i32 0, i32* %"ret"
  store i32 10, i32* @"a"
  %".4" = load i32, i32* @"a"
  store i32 %".4", i32* %"b"
  %".6" = load i32, i32* @"a"
  store i32 %".6", i32* @"a"
  br label %"fim_main"
fim_main:
  %".9" = load i32, i32* %"ret"
  ret i32 %".9"
}
