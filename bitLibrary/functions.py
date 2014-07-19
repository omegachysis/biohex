
def _nucleotidesToNumerals(nucleotides):
    nums = []
    for nuc in nucleotides:
        nums.append(('a','t','c','g').index(nuc.lower()))
    return nums

def _baseFourToChar(nums):
    val = 0
    nums.reverse()
    for i in range(4):
        val += int(nums[i]) * ( 4 ** i)
    return chr(val)

def _charToBaseFour(char):
    val = ord(char)
    nums = []
    for i in list(range(4)).__reversed__():
        divides = val // (4 ** i)
        val -= divides * (4 ** i)
        nums.append(divides)
    return nums

def _convertDNA(dna):
    nums = _nucleotidesToNumerals(dna)
    rna = ""
    frame = []
    FRAME_WIDTH = 4
    for num in nums:
        frame.append(num)
        if len(frame) == FRAME_WIDTH:
            rna += _baseFourToChar(frame)
            frame = []
    return rna

def _convertRNA(rna):
    dna = ""
    for char in rna:
        for num in _charToBaseFour(char):
            dna += "ATCG"[num]
    return dna
