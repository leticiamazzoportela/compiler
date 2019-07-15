; ModuleID = "meu_modulo.bc"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"() 
{
iniciomain:
  %"ret" = alloca i32
  %"y" = alloca double, align 4
  %"x" = alloca i32, align 4
  %".2" = call i32 (...) @"scanf"([3 x i8]* @"leia2", i32 y)
  %".3" = call i32 (...) @"printf"([4 x i8]* @"escreva3", i32 y)
  %".4" = uitofp i32 0.0 to double
  store double %".4", double* %"y"
  store i32 0, i32* %"x"
  %".7" = call i32 (...) @"printf"([4 x i8]* @"escreva4", i32 x)
  %".8" = call i32 (...) @"scanf"([3 x i8]* @"leia5", i32 x)
  store i32 0, i32* %"ret"
  br label %"fimmain"
fimmain:
  %".11" = load i32, i32* %"ret"
  ret i32 %".11"
}

@"leia2" = constant [3 x i8] c"%d\00"
declare i32 @"scanf"(...) 

@"escreva3" = constant [4 x i8] c"%d\0a\00"
declare i32 @"printf"(...) 

@"escreva4" = constant [4 x i8] c"%d\0a\00"
@"leia5" = constant [3 x i8] c"%d\00"