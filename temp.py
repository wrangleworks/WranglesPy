import wrangles


recipe = """
read:
  - test:
      rows: 5
      values:
        header1: a
        header2: b
        header3: <word>

wrangles:
  - expression:
      input: header1 in header3
      output: result

  - log: {}
"""

wrangles.recipe.run(recipe)