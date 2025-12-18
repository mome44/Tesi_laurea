


*******BLEU*******
N gram precision 
![[Screenshot 2025-12-11 162409.png]]

Brevity penalty

Penalizes short translations:
![[Screenshot 2025-12-11 162404.png]]

where:
- c = length of candidate translation
- r = effective reference length

![[Screenshot 2025-12-11 162354.png]]
Wn = 1/N 
BLEU uses N=4