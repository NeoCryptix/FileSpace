import random
import json
#import sys
import os
import requests
import time
import platform
from datetime import datetime

configpath = "config.json"
debug = True
lineOn = 0


def fetch(modulefile, modulename):
  st = time.time()
  url = f"https://filespace.neocryptix.repl.co/files/{modulefile}"
  r = requests.get(url, stream=True)
  with open(f"{modulefile}", "wb") as mod:
    for chunk in r.iter_content(chunk_size=1024):
      if chunk:
        mod.write(chunk)
  end = time.time()
  tme = round(end - st, 3)
  if debug:
    print(
      f"[{lineOn}] fetchModule:",
      modulename,
      "installed from Filespace in",
      tme,
      "s",
    )
  if not debug:
    print(f"{modulename} installed in {tme}s")


def getConfig(configpath):
  try:
    with open(configpath) as config:
      data = json.load(config)
      
    debug = data["debugMode"]
    debugSys = data["debugSys"]
    run = data["runFile"]
    inter = data["interpreterFile"]
    comment = data["commentChar"]
    walsh = data["walshMode"]
    delay = data["commandDelay"]
    log = data["logFile"]

    return debug, debugSys, run, inter, comment, walsh, delay, log
  except json.decoder.JSONDecodeError:
    print("[0] configInvalidError: config.json invalid; file restored to defaults")
    fetch("config.json", "restoreConfig")
    return getConfig(configpath)
  except FileNotFoundError:
    print("[0] configInvalidError: config.json missing; file restored to defaults")
    fetch("config.json", "restoreConfig")
    return getConfig(configpath)


variables = {}
functions = {}
checks = {}
functions.update({"variables": variables, "functions": functions})
isVar = None

debug, debugSys, run, inter, comment, walsh, delay, log = getConfig(configpath)

if debug:
  file1 = open(log, "a")
  now = datetime.now()
  file1.write(f"\n\n[0] {now}")
  osname = platform.platform()
  osarch = platform.architecture()
  osmach = platform.machine()
  osarch1 = osarch[0]
  pyver = platform.python_build()
  pyver0 = pyver[0]
  pyver1 = pyver[1]
  delay2 = float(delay)

  time.sleep(delay2)
  print(f"[0] configFile: {configpath}")
  file1.write(f"\n[0] configFile: {configpath}")

  time.sleep(delay2)
  print(f"[0] runFile: {run}")
  file1.write(f"\n[0] runFile: {run}")

  time.sleep(delay2)
  print(f"[0] logFile: {log}")
  file1.write(f"\n[0] logFile: {log}")

  if debugSys:
    time.sleep(delay2)
    print(f"[0] operSys: {osname}; {osarch1}; {osmach}")
    file1.write(f"\n[0] operSys: {osname}; {osarch1}; {osmach}")

  if debugSys:
    time.sleep(delay2)
    print(f"[0] pyBuild: {pyver0}; {pyver1}")
    file1.write(f"\n[0] pyBuild: {pyver0}; {pyver1}")

  time.sleep(delay2)


def error(type):
  if type == "syntax":
    raise SyntaxError


file = open(run, "r+")
content = file.readlines()


def interpret(content):
  file1 = open(log, "a")
  isVar = False
  _if = 0
  executeFirstIndent = False
  executeSecondIndent = False
  indent = 0
  lineOn = 1
  for line in content:
    line.replace("\n", "")
    line.replace("\n", "")
    if line[0:6] == "output":
      output = ""
      line = [x for x in line]
      del line[0:6]
      line.remove("(")
      line.remove(")")
      try:
        line.remove("\n")
      except:
        pass
      if line[0] != "'" and line[-1] != "'":
        isVar = True
      elif line[0] == "'" and line[-1] == "'":
        isVar = False
      cont = ""
      for i in line:
        cont += i
      if "' + " in cont:
        try:
          line = cont.split(" + ")
          sp = True
        except:
          sp = False
        if sp:
          isVar = "combo"
          var = line[1]
          line.pop(1)
          text = line[0]
          ntext = [x for x in text]
          try:
            ntext.remove("'")
            ntext.remove("'")
          except:
            pass
          text = ""
          for i in ntext:
            text += i
      if isVar == False:
        try:
          line.remove("'")
          line.remove("'")
        except:
          pass
      elif isVar == True:
        varName = ""
        varName = varName.join(line)
        line = variables[varName]
      if isVar == False:
        if debug:
          print(f"[{lineOn}] outputMsg:", output.join(line))
          file1.write(f"\n[{lineOn}] outputMsg: {output.join(line)}")
        else:
          print(output.join(line))
      elif isVar == True:
        if debug:
          print(f"[{lineOn}] outputVar:", line)
          file1.write(f"\n[{lineOn}] outputVar: {line}")
        else:
          print(line)
      elif isVar == "combo":
        if debug:
          message = f"[{lineOn}] outputMsg+Var: {text}{variables[var]}"
          print(message)
          file1.write(f"\n[{lineOn}] outputMsg+Var: {text}{variables[var]}")
        else:
          message = f"{text}{variables[var]}"
          print(message)

    elif " = input(" in line:
      line = line.split(" = ")
      name = line[0]
      line.pop(0)
      cont = ""
      cont = cont.join(line)
      cont = [x for x in cont]
      for i in [0, 0, 0, 0, 0, 0, 0, -1, -1, -1]:
        cont.pop(i)
      prompt = ""
      for i in cont:
        prompt += i
      if debug:
        if prompt[-1] != " ":
          prompt += " "
        value = input(f"[{lineOn}] inputAsk: {prompt}")
        file1.write(f"\n[{lineOn}] inputAsk: {prompt}")
      else:
        if prompt[-1] != " ":
          prompt += " "
        value = input(prompt)
      variables.update({name: value})
      if debug:
        prompt = prompt[:-1]
        print(f"[{lineOn}] getInput: {prompt}; response:", value)
        file1.write(f"\n[{lineOn}] getInput: {prompt}; response: {value}")
    elif comment in line:
      if debug:
        commenttxt = f"[{lineOn}] commentNoCode:" + line.replace(comment, "").replace("\n", "")
        print(commenttxt)
        file1.write(commenttxt)
    elif "= new" in line:
      name = ""
      value = None
      line = line.split(" = ")
      name = line[0]
      line.pop(0)
      cont = line[0]
      cont = [x for x in cont]
      try:
        cont.remove("\n")
      except:
        pass
      torem = ["n", "e", "w", "(", ")"]
      for let in torem:
        cont.remove(let)
      if cont[0] == "f":
        filet = ""
        for i in [-1, -1, 0, 0, 0, 0, 0, 0]:
          cont.pop(i)
        for i in cont:
          filet += i
        name += "()"
        functions.update({name: filet})
        if debug:
          print(f"[{lineOn}] createFunc: {name}")
          file1.write(f"\n[{lineOn}] createFunc: {name}")
      if cont[0] == "i":
        for i in [0, 0, 0]:
          cont.pop(i)
        cont.pop(-1)
        cont.pop(0)
        num = ""
        for i in cont:
          num += i
        variables.update({name: num})
        if debug:
          print(f"[{lineOn}] createInt:", name)
          file1.write(f"\n[{lineOn}] createInt: {name}")
      elif cont[0] == "s":
        for i in [0, 0, 0]:
          cont.pop(i)
        torem = ["(", ")"]
        for let in torem:
          cont.remove(let)
        str = ""
        for i in cont:
          str += i
        variables.update({name: str})
        if debug:
          print(f"[{lineOn}] createStr:", name)
          file1.write(f"\n[{lineOn}] createStr: {name}")
      elif cont[0] == "r":
        for i in [0, 0, 0, 0, 0, 0, 0]:
          cont.pop(i)
        for i in cont:
          if not i.isnumeric():
            cont.remove(i)
        #cont.remove("n")
        #cont.remove(")")
        contn = ""
        contn = contn.join(cont)
        cont = contn.split(" ")
        for idx, i in enumerate(cont):
          cont[idx] = eval(i)
        min = cont[0]
        max = cont[1]
        num = random.randint(min, max)
        variables.update({name: num})
        if debug:
          print(f"[{lineOn}] createRandInt:", name, f"[{min}, {max}]")
          file1.write(f"\n[{lineOn}] createRandInt: {name} [{min}, {max}]")
      elif cont[0] == "b":
        for i in [0, 0, 0, 0]:
          cont.pop(i)
        torem = ["(", ")"]
        for let in torem:
          cont.remove(let)
        bool = ""
        for i in cont:
          bool += i
        if bool == "True":
          bool = True
        else:
          bool = False
        variables.update({name: bool})
        if debug:
          print(f"[{lineOn}] createBool:", name)
          file1.write(f"\n[{lineOn}] createBool: {name}")
    elif "exec" in line:
      line = [x for x in line]
      if line[4] == "(":
        torun = ""
        for i in [0, 0, 0, 0]:
          line.pop(i)
        line.pop(-1)
        line.pop(-1)
        line.pop(0)
        line.pop(0)
        for i in line:
          torun += i
        file = open(run, "r+")
        content = file.readlines()
        interpret(content)
    elif "wait(" in line:
      line = [x for x in line]
      for i in [0, 0, 0, 0, -1, -1, 0]:
        line.pop(i)
      linen = ""
      for i in line:
        linen += i
      timee = eval(linen)
      if debug:
        print(f"[{lineOn}] waitTime:", timee, "s")
        file1.write(f"\n[{lineOn}] waitTime: {timee} s")
      time.sleep(timee)
    elif "check(" in line:
      result = None
      line = [x for x in line]
      for i in [0, 0, 0, 0, 0, 0, -1, -1]:
        line.pop(i)
      first = ""
      second = ""
      linen = ""
      for i in line:
        linen += i
      line = linen.split(" = ")
      first = line[0]
      second = line[-1]
      if second.isnumeric():
        second = eval(second)
      if variables[first] == second:
        result = True
        if debug:
          expression = f"{first} = {second}"
          print(f"[{lineOn}] checkIf {expression}, equalTrue")
          file1.write(f"\n[{lineOn}] checkIf {expression}, equalTrue")
      else:
        result = False
        if debug:
          expression = f"{first} = {second}"
          print(f"[{lineOn}] checkIf: {expression}, equalFalse")
          file1.write(f"\n[{lineOn}] checkIf: {expression}, equalFalse")
      checks.update({lineOn: result})
    elif "toInt(" in line:
      line = [x for x in line]
      for i in [0, 0, 0, 0, 0, -1, -1, 0]:
        line.pop(i)
      toint = ""
      for i in line:
        toint += i
      fdb = toint
      vToInt = variables[toint]
      int = eval(vToInt)
      variables.update({toint: int})
      if debug:
        print(f"[{lineOn}] toInt:", fdb)
        file1.write(f"\n[{lineOn}] toInt: {fdb}")
    elif line in functions.keys():
      file = functions[line]
      filet = open(file, "r+")
      cont = filet.readlines()
      filet.close()
      print(f"[{lineOn}] execFunc", line)
      file1.write(f"\n[{lineOn}] execFunc {line}")
      interpret(cont)
    elif line.replace("\n", "") == "":
      if debug:
        print(f"[{lineOn}] lineEmpty")
        file1.write(f"\n[{lineOn}] lineEmpty")
    elif lineOn - 1 in checks:
      # If True
      _if = 1
      if checks[lineOn - 1] == True:
        executeFirstIndent = True
    elif _if == 1 and lineOn - 3 in checks:
      # If False
      _if = 0
      if checks[lineOn - 3] == False:
        executeSecondIndent = True
    elif "  " in line:
      indent += 1
      if indent == 1 and executeFirstIndent:
        if debug:
          print(f"[{lineOn}] execFirstIndent")
          file1.write(f"\n[{lineOn}] execFirstIndent")
        lineto = [line.replace("  ", "")]
        interpret(lineto)
      elif indent == 2 and executeSecondIndent:
        if debug:
          print(f"[{lineOn}] execSecondIndent")
          file1.write(f"\n[{lineOn}] execSecondIndent")
        lineto = [line.replace("  ", "")]
        interpret(lineto)
    elif "walsh(r)" in line and walsh:
      randwalsh = ["0", "1", "2", "3"]
      choice = random.choice(randwalsh)
      if choice == "0":
        walshmsg = "Hit the children!"
      if choice == "1":
        walshmsg = "MWITG!"
      if choice == "2":
        walshmsg = "It was an accident!"
      if choice == "3":
        walshmsg = "I was just stretching."
      if not debug:
        print(walshmsg)
      elif debug:
        print(f"[{lineOn}] walshCommand: {walshmsg}")
        file1.write(f"\n[{lineOn}] walshCommand: {walshmsg}")
    elif "walsh(0)" in line and walsh:
      if not debug:
        print("Hit the children!")
      elif debug:
        print(f"[{lineOn}] walshCommand: Hit the children!")
        file1.write(f"[{lineOn}] walshCommand: Hit the children!")
    elif "walsh(1)" in line and walsh:
      if not debug:
        print("MWITG!")
      elif debug:
        print(f"[{lineOn}] walshCommand: MWITG!")
        file1.write(f"\n[{lineOn}] walshCommand: MWITG!")
    elif "walsh(2)" in line and walsh:
      if not debug:
        print("It was an accident!")
      elif debug:
        print(f"[{lineOn}] walshCommand: It was an accident!")
        file1.write(f"\n[{lineOn}] walshCommand: It was an accident!")
    elif "walsh(3)" in line and walsh:
      if not debug:
        print("I was just stretching.")
      elif debug:
        print(f"[{lineOn}] walshCommand: I was just stretching.")
        file1.write(f"\n[{lineOn}] walshCommand: I was just stretching.")
    elif "clearConsole()" in line:
      osx = platform.system()
      if osx == "Linux":
        os.system("clear")
      elif osx == "Windows":
        os.system("cls")
      else:
        os.system("clear")
      if debug:
        print (f"[{lineOn}] clearConsole")
        file1.write(f"\n[{lineOn}] clearConsole")
    else:
      if debug:
        line = line.replace("\n", "")
        print(f'[{lineOn}] noSyntax: "{line}"')
        file1.write(f'\n[{lineOn}] noSyntax: "{line}"')
    lineOn += 1
    time.sleep(delay)


if not walsh:
  if debug:
    print("[0] walshNotEnabled: program may be unstable")
    file1.write("[0] walshNotEnabled: program may be unstable")

interpret(content)
if debug:
  file1.close()