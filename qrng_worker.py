import json
import sys
import qsharp

QSHARP_CODE = r"""
import Std.Convert.*;
import Std.Math.*;

operation GenerateRandomBit() : Result {
    use q = Qubit();
    H(q);
    let result = M(q);
    Reset(q);
    return result;
}

operation GenerateRandomNumberInRange(max : Int) : Int {
    mutable bits = [];
    let nBits = BitSizeI(max);

    for _ in 1..nBits {
        set bits += [GenerateRandomBit()];
    }

    let sample = ResultArrayAsInt(bits);
    return sample > max ? GenerateRandomNumberInRange(max) | sample;
}
"""

def main():
    max_value = int(sys.argv[1])
    n_samples = int(sys.argv[2])

    # Define Q# in THIS process
    qsharp.eval(QSHARP_CODE)

    # Generate samples
    results = [qsharp.eval(f"GenerateRandomNumberInRange({max_value})") for _ in range(n_samples)]
    print(json.dumps(results))

if __name__ == "__main__":
    main()
