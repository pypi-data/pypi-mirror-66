import torch

bart = torch.hub.load('pytorch/fairseq', 'bart.large.cnn')
bart.cuda()
bart.eval()
bart.half()
count = 1
bsz = 2

with open('test.source') as source, open('test.hypo', 'w') as fout:
    sline = source.readline().strip()
    slines = [sline]
    for sline in source:
        if count % bsz == 0:
            with torch.no_grad():
                hypotheses_batch = bart.sample(slines, beam=4, lenpen=2.0, max_len_b=520, min_len=55, no_repeat_ngram_size=3)

            for hypothesis in hypotheses_batch:
                fout.write(hypothesis + '\n')
                fout.flush()
            slines = []

        slines.append(sline.strip())
        count += 1
    if slines != []:
        hypotheses_batch = bart.sample(slines, beam=4, lenpen=2.0, max_len_b=520, min_len=55, no_repeat_ngram_size=3)
        for hypothesis in hypotheses_batch:
            fout.write(hypothesis + '\n')
            fout.flush()


