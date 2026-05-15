import streamlit as st
import matplotlib.pyplot as plt
import subprocess
import sys
import json

st.set_page_config(page_title="Quantum RNG (Q# + Python)", layout="centered")
st.title("Quantum Random Number Generator")

st.write(
    "This app generates random numbers using Q# and visualizes the distribution. "
    "The quantum runtime runs in a separate process to avoid Streamlit thread issues."
)

# Controls
max_value = st.slider("Max Value", min_value=1, max_value=1024, value=100)
n_samples = st.slider("Number of Samples", min_value=10, max_value=2000, value=200, step=10)

if st.button("Generate Random Numbers"):
    with st.spinner("Generating..."):
        try:
            # Call the worker using the SAME python executable Streamlit is running under
            output = subprocess.check_output(
                [sys.executable, "qrng_worker.py", str(max_value), str(n_samples)],
                text=True,
                stderr=subprocess.STDOUT
            )

            results = json.loads(output)

            st.write("Sample Output (first 10):", results[:10])

            fig, ax = plt.subplots()
            ax.hist(results, bins=10)
            ax.set_title(f"Distribution (0–{max_value})")
            ax.set_xlabel("Value")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

        except subprocess.CalledProcessError as e:
            st.error("Worker crashed. Output below:")
            st.code(e.output)

        except json.JSONDecodeError:
            st.error("Worker output was not valid JSON. Output below:")
            st.code(output)

        except Exception as e:
            st.error(f"Unexpected error: {e}")