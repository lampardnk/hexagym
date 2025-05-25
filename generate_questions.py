import json
import requests

# Sample questions with carefully crafted content
questions = [
    {
        "name": "Basic RC Circuit Analysis",
        "tags": [
            {"type": "level", "value": "A-Level"},
            {"type": "topic", "value": "Physics"},
            {"type": "type", "value": "Short Answer"}
        ],
        "points": 8,
        "content": r"""
Consider the RC circuit shown below:

\begin{circuitikz}
\draw
  (0,0) node[ground] {}
  to[V, l=$12\text{V}$] (0,3)
  to[R, l=$2\text{k}\Omega$] (3,3)
  to[C, l=$4\mu\text{F}$] (3,0)
  -- (0,0);
\end{circuitikz}

Calculate:
a) The initial current when the circuit is first connected
b) The time constant of the circuit
c) The voltage across the capacitor after one time constant
""",
        "hints": [
            {
                "text": "For initial current, treat the capacitor as a short circuit initially",
                "points_deduction": 2
            },
            {
                "text": "Time constant τ = RC",
                "points_deduction": 2
            },
            {
                "text": "After one time constant, Vc = 0.63 × V_final",
                "points_deduction": 2
            }
        ],
        "answer": "test"
    },
    {
        "name": "Vector Addition in 2D",
        "tags": [
            {"type": "level", "value": "O-Level"},
            {"type": "topic", "value": "Math"},
            {"type": "type", "value": "Short Answer"}
        ],
        "points": 6,
        "content": r"""
Consider the following vectors:

\begin{tikzpicture}
\draw[->] (0,0) -- (2,0) node[right] {$\vec{a} = 2\hat{i}$};
\draw[->] (0,0) -- (0,2) node[above] {$\vec{b} = 2\hat{j}$};
\draw[dashed] (2,0) -- (2,2) -- (0,2);
\end{tikzpicture}

Find:
a) The magnitude of $\vec{a} + \vec{b}$
b) The angle between $\vec{a}$ and $\vec{a} + \vec{b}$
""",
        "hints": [
            {
                "text": "Use the Pythagorean theorem to find the magnitude",
                "points_deduction": 1
            },
            {
                "text": "The angle can be found using tan⁻¹(opposite/adjacent)",
                "points_deduction": 2
            }
        ],
        "answer": "test"
    },
    {
        "name": "Simple Op-Amp Inverting Amplifier",
        "tags": [
            {"type": "level", "value": "A-Level"},
            {"type": "topic", "value": "Physics"},
            {"type": "type", "value": "Short Answer"}
        ],
        "points": 7,
        "content": r"""
Analyze the inverting amplifier circuit:

\begin{circuitikz}
\draw
  (0,0) node[op amp] (opamp) {}
  (opamp.-) to[R, l=$10\text{k}\Omega$] ++(-2,0) node[left] {$V_{in}$}
  (opamp.-) to[R, l=$20\text{k}\Omega$] (opamp.out)
  (opamp.+) -- ++(0,-1) node[ground] {};
\end{circuitikz}

If $V_{in} = 2V$:
a) What is the gain of the amplifier?
b) What is the output voltage $V_{out}$?
""",
        "hints": [
            {
                "text": "For inverting amplifier, gain = -Rf/Rin",
                "points_deduction": 2
            },
            {
                "text": "Remember the negative sign in the gain formula",
                "points_deduction": 1
            }
        ],
        "answer": "test"
    },
    {
        "name": "Basic Logic Gate Circuit",
        "tags": [
            {"type": "level", "value": "IBDP"},
            {"type": "topic", "value": "Computer Science"},
            {"type": "type", "value": "Short Answer"}
        ],
        "points": 5,
        "content": r"""
Consider the logic circuit below:

\begin{circuitikz}
\draw
  (0,2) node[and port] (and1) {}
  (0,0) node[not port] (not1) {}
  (and1.in 1) node[left] {A}
  (not1.in) node[left] {B}
  (not1.out) -- (and1.in 2)
  (and1.out) node[right] {Y};
\end{circuitikz}

Complete the truth table for inputs A and B, and output Y.
""",
        "hints": [
            {
                "text": "First find the output of the NOT gate for each input B",
                "points_deduction": 1
            },
            {
                "text": "Then combine with input A using AND gate",
                "points_deduction": 2
            }
        ],
        "answer": "test"
    },
    {
        "name": "Geometric Transformations",
        "tags": [
            {"type": "level", "value": "O-Level"},
            {"type": "topic", "value": "Math"},
            {"type": "type", "value": "Short Answer"}
        ],
        "points": 6,
        "content": r"""
Consider triangle ABC:

\begin{tikzpicture}
\draw[thick] (0,0) -- (2,0) -- (1,2) -- cycle;
\node[below] at (0,0) {A};
\node[below] at (2,0) {B};
\node[above] at (1,2) {C};
\draw[dashed] (3,0) -- (5,0) -- (4,2) -- cycle;
\end{tikzpicture}

The dashed triangle is a transformation of triangle ABC.
Identify the transformation and specify its parameters.
""",
        "hints": [
            {
                "text": "Compare the position of corresponding vertices",
                "points_deduction": 1
            },
            {
                "text": "Check if the shape's size and orientation are preserved",
                "points_deduction": 2
            }
        ],
        "answer": "test"
    },
    {
        "name": "Simple Harmonic Motion",
        "tags": [
            {"type": "level", "value": "A-Level"},
            {"type": "topic", "value": "Physics"},
            {"type": "type", "value": "Short Answer"}
        ],
        "points": 7,
        "content": r"""
A mass on a spring oscillates as shown:

\begin{tikzpicture}
\draw[->] (-3,0) -- (3,0) node[right] {x};
\draw[->] (0,-2) -- (0,2) node[above] {y};
\draw[domain=-2:2,smooth,variable=\x,blue] plot ({\x},{1.5*sin(\x r)});
\draw[fill=red] (1,{1.5*sin(1 r)}) circle (0.1);
\end{tikzpicture}

Given amplitude A = 1.5m and period T = 2s:
a) Write the equation of motion y(t)
b) Calculate the maximum velocity
""",
        "hints": [
            {
                "text": "The general equation is y = A sin(ωt)",
                "points_deduction": 2
            },
            {
                "text": "Angular frequency ω = 2π/T",
                "points_deduction": 2
            }
        ],
        "answer": "test"
    },
    {
        "name": "Chemical Equilibrium",
        "tags": [
            {"type": "level", "value": "IBDP"},
            {"type": "topic", "value": "Chemistry"},
            {"type": "type", "value": "Short Answer"}
        ],
        "points": 8,
        "content": r"""
Consider the equilibrium:

\begin{tikzpicture}
\draw[->] (0,1) -- (4,1);
\draw[<-] (0,0) -- (4,0);
\node at (2,1.5) {$\text{N}_2 + 3\text{H}_2$};
\node at (2,-0.5) {$2\text{NH}_3$};
\node at (2,0.5) {$K_c = 4.2$};
\end{tikzpicture}

If [N₂] = 0.5M and [H₂] = 0.3M at equilibrium:
Calculate [NH₃] at equilibrium.
""",
        "hints": [
            {
                "text": "Use the Kc expression: Kc = [NH₃]²/([N₂][H₂]³)",
                "points_deduction": 2
            },
            {
                "text": "Substitute the known values and solve for [NH₃]",
                "points_deduction": 2
            }
        ],
        "answer": "test"
    },
    {
        "name": "Basic Network Topology",
        "tags": [
            {"type": "level", "value": "IBDP"},
            {"type": "topic", "value": "Computer Science"},
            {"type": "type", "value": "Short Answer"}
        ],
        "points": 6,
        "content": r"""
Analyze the network topology:

\begin{tikzpicture}
\draw (0,0) node[circle,draw] (A) {A};
\draw (2,0) node[circle,draw] (B) {B};
\draw (1,2) node[circle,draw] (C) {C};
\draw (A) -- (B) -- (C) -- (A);
\end{tikzpicture}

a) Identify the topology type
b) How many connections are needed for n nodes?
c) What happens if one connection fails?
""",
        "hints": [
            {
                "text": "Each node connects to exactly two others",
                "points_deduction": 1
            },
            {
                "text": "For n nodes, count the number of edges",
                "points_deduction": 2
            }
        ],
        "answer": "test"
    },
    {
        "name": "Economic Supply-Demand Curve",
        "tags": [
            {"type": "level", "value": "A-Level"},
            {"type": "topic", "value": "Economics"},
            {"type": "type", "value": "Short Answer"}
        ],
        "points": 7,
        "content": r"""
Analyze the supply-demand curves:

\begin{tikzpicture}
\draw[->] (0,0) -- (5,0) node[right] {Quantity};
\draw[->] (0,0) -- (0,5) node[above] {Price};
\draw[blue] (0,4) -- (4,1) node[right] {D};
\draw[red] (0,1) -- (4,4) node[right] {S};
\end{tikzpicture}

Find:
a) Equilibrium point
b) Effect of 1-unit rightward shift of supply curve
""",
        "hints": [
            {
                "text": "Equilibrium is where supply meets demand",
                "points_deduction": 2
            },
            {
                "text": "A rightward shift decreases price and increases quantity",
                "points_deduction": 2
            }
        ],
        "answer": "test"
    },
    {
        "name": "Magnetic Field Lines",
        "tags": [
            {"type": "level", "value": "A-Level"},
            {"type": "topic", "value": "Physics"},
            {"type": "type", "value": "Short Answer"}
        ],
        "points": 6,
        "content": r"""
A current-carrying wire creates a magnetic field:

\begin{tikzpicture}
\draw[thick] (0,-2) -- (0,2);
\draw[->] (0,0) node[circle,fill,inner sep=2pt] {} circle (1);
\draw[->] (0,0) circle (1.5);
\draw[->] (0,0) circle (2);
\node[above] at (0,2) {I};
\end{tikzpicture}

a) State the direction of the magnetic field
b) How does field strength vary with distance?
""",
        "hints": [
            {
                "text": "Use the right-hand grip rule",
                "points_deduction": 1
            },
            {
                "text": "B ∝ 1/r relationship",
                "points_deduction": 2
            }
        ],
        "answer": "test"
    }
]

def post_question(question):
    try:
        response = requests.post('http://localhost:5000/questions', json=question)
        if response.status_code == 200:
            print(f"Successfully added question: {question['name']}")
        else:
            print(f"Failed to add question: {question['name']}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error posting question: {str(e)}")

def main():
    print("Starting to generate questions...")
    for question in questions:
        post_question(question)
    print("Finished generating questions.")

if __name__ == "__main__":
    main() 