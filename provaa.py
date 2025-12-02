import re
testo = "Abetone è nu comune 'e 707 crestiane d’’a pruvincia 'e Pistoia."
pattern = re.compile(
    r"^[A-ZÀ-Üa-zà-ü'’ \-]+ è nu comune\b.*?pruvincia\b.*$",
    re.MULTILINE
)

testo_filtrato = re.sub(pattern, "", testo)
print(testo_filtrato)