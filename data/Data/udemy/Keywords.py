# make a keywords dictnoary
import pandas as pd

Keywords = [
    # add 25 programming languages
    "python", "java", "c++", "c#", "javascript", "php", "swift", "kotlin", "go", "ruby", "scala", "rust", "typescript",
    "dart", "perl", "r", "matlab", "assembly", "fortran", "cobol", "lisp", "haskell", "erlang", "prolog", "clojure",
]

# save keywords list to keywords.txt file using pandas
df = pd.DataFrame(Keywords)
df.to_csv("data/Data/udemy/keywords.txt", index=False)