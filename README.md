# Divine Whisper Merge Helper

Automates safe merging of four branches into main in the divine-whisper-ecosystem repo.

**Branches merged (in order)**  
1. repo-ecos  
2. post-launch  
3. spec-v7  
4. ray-poc

**Usage**

```bash
git clone https://github.com/aruintelligence/divine-whisper-merge-helper.git
cd divine-whisper-merge-helper
python merge_four_branches.py --workspace ./tmp-merge
