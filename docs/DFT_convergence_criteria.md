# DFT Convergence Criteria (Quantum ESPRESSO)

Three criteria used to decide whether a Quantum ESPRESSO calculation has successfully converged,
and their physical meaning.

---

## 1. Electronic (SCF) convergence
Termination condition of the self-consistent-field loop that finds the electronic ground state.
- **Parameter:** `conv_thr` (convergence threshold)
- **Typical value:** 1.0×10⁻⁶ – 1.0×10⁻⁸ Ry
- **Meaning:** the difference between input (ρ_in) and output (ρ_out) charge density must fall below
  this value; SCF stops when the *estimated scf accuracy* drops below `conv_thr`.
- **Reference:** Giannozzi et al., *J. Phys.: Condens. Matter* **21**, 395502 (2009) (the QE paper).

## 2. Ionic convergence (geometry optimization)
For `relax`, the criterion that atoms have reached equilibrium positions.
- **Energy:** `etot_conv_thr` — typical 1.0×10⁻⁴ Ry. The total-energy change between steps must be
  below this value (energy has bottomed out).
- **Force:** `forc_conv_thr` — typical 1.0×10⁻³ Ry/Bohr. The force on every atom must be below this
  value (atoms have no reason to move further).
- Both must be satisfied for the BFGS optimizer to terminate.

## 3. Cell convergence (variable-cell relaxation)
Additional criterion for `vc-relax` (optimizing cell volume/shape).
- **Pressure:** `press_conv_thr` — typical 0.5 kbar (0.5–1.0 kbar). The system stress must approach
  the target pressure (usually 0).
- **Note:** `vc-relax` is the most demanding because force and pressure must converge simultaneously.

---

## Summary checklist

| Quantity | Parameter | Recommended | Meaning |
|---|---|---|---|
| Electronic | `conv_thr` | 1.0d-6 Ry | charge density self-consistent |
| Energy | `etot_conv_thr` | 1.0d-4 Ry | energy no longer changing |
| Force | `forc_conv_thr` | 1.0d-3 Ry/Bohr | atoms no longer moving |
| Pressure | `press_conv_thr` | 0.5 kbar | cell size fixed |

Only when all applicable conditions are met does QE print **"JOB DONE"**.

> Note for this system (Ni-whitlockite): near-degenerate high/low-spin Ni causes charge sloshing and
> spin frustration. This is mitigated by a 42-atom primitive cell and a 2-step protocol
> (`nspin=1` geometry relaxation → `nspin=2` energy evaluation).
