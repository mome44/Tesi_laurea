input_file = "ferri_le_fiabe.txt"
output_file = "ferri_le_fiabe_pari.txt"

with open(input_file, "r", encoding="utf-8") as f_in, \
     open(output_file, "w", encoding="utf-8") as f_out:

    for i, riga in enumerate(f_in, start=1):
        if i % 2 == 0: 
            f_out.write(riga)