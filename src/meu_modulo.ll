; ModuleID = "meu_modulo.bc"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"soma"(i32 %"a", i32 %"b") 
{
inicio_soma:
  %"a.1" = alloca i32, align 4
  store i32 %"a", i32* %"a.1"
  %"b.1" = alloca i32, align 4
  store i32 %"b", i32* %"b.1"
  %"ret" = alloca i32
  %"b.2" = alloca i32, align 4
  %"a.2" = alloca i32, align 4
  %"c" = alloca i32, align 4
  %"addInt" = add i32 a, b
  store i32 %"addInt", i32* %"ret"
  store i32 0, i32* %"ret"
  %".8" = load i32, i32* %"a.2"
  %".9" = load i32, i32* %"b.2"
  %".10" = call i32 @"soma"(i32 %".8", i32 %".9")
  store i32 %".10", i32* %"c"
  %".12" = load i32, i32* %"a.2"
  %".13" = load i32, i32* %"b.2"
  %".14" = call i32 @"soma"(i32 %".12", i32 %".13")
  %".15" = load i32, i32* %"a.2"
  %".16" = call i32 (...) @"printf"([4 x i8]* @"escreva2", i32 %".15")
  %".17" = load i32, i32* %"b.2"
  %".18" = call i32 (...) @"printf"([4 x i8]* @"escreva3", i32 %".17")
  %".19" = load i32, i32* %"c"
  %".20" = call i32 (...) @"scanf"([3 x i8]* @"leia4", i32 %".19")
  br label %"fim_soma"
fim_soma:
  %".22" = load i32, i32* %"ret"
  ret i32 %".22"
}

@"escreva2" = constant [4 x i8] c"%d\0a\00"
declare i32 @"printf"(...) 

@"escreva3" = constant [4 x i8] c"%d\0a\00"
@"leia4" = constant [3 x i8] c"%d\00"
declare i32 @"scanf"(...) 

define i32 @"main"() 
{
inicio_main:
  %"ret" = alloca i32
  %"b" = alloca i32, align 4
  %"a" = alloca i32, align 4
  %"c" = alloca i32, align 4
  %"addInt" = add i32 a, b
  store i32 %"addInt", i32* %"ret"
  store i32 0, i32* %"ret"
  %".4" = load i32, i32* %"a"
  %".5" = load i32, i32* %"b"
  %".6" = call i32 @"soma"(i32 %".4", i32 %".5")
  store i32 %".6", i32* %"c"
  %".8" = load i32, i32* %"a"
  %".9" = load i32, i32* %"b"
  %".10" = call i32 @"soma"(i32 %".8", i32 %".9")
  %".11" = load i32, i32* %"a"
  %".12" = call i32 (...) @"printf"([4 x i8]* @"escreva5", i32 %".11")
  %".13" = load i32, i32* %"b"
  %".14" = call i32 (...) @"printf"([4 x i8]* @"escreva6", i32 %".13")
  %".15" = load i32, i32* %"c"
  %".16" = call i32 (...) @"scanf"([3 x i8]* @"leia7", i32 %".15")
  br label %"fim_main"
fim_main:
  %".18" = load i32, i32* %"ret"
  ret i32 %".18"
}

@"escreva5" = constant [4 x i8] c"%d\0a\00"
@"escreva6" = constant [4 x i8] c"%d\0a\00"
@"leia7" = constant [3 x i8] c"%d\00"