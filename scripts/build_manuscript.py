"""Build a standalone Markdown manuscript; no TeX toolchain is involved."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
paper=(ROOT/'paper.md').read_text(encoding='utf-8')
theory=(ROOT/'THEORY.md').read_text(encoding='utf-8')
start=paper.index('## Appendix A. Proofs and implementation definitions')
end=paper.index('## Appendix B. Reproduction and audit material')
theory=theory.split('\n',1)[1].lstrip()
theory=re.sub(r'^(#{2,5}) ',r'\1# ',theory,flags=re.MULTILINE)
appendix='## Appendix A. Complete proofs and implementation definitions\n\nSection and theorem numbers within this appendix are local to the appendix.\n\n'+theory+'\n\n'
result=paper[:start]+appendix+paper[end:]
for target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',result):
    assert (ROOT/target).is_file(),f'Missing figure: {target}'
assert 'should be integrated verbatim' not in result
(ROOT/'manuscript.md').write_text(result,encoding='utf-8')
print('manuscript.md:',len(result.split()),'words; complete proof appendix included')
