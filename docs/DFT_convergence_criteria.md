# DFT 수렴 조건 및 판단 기준 (Convergence Criteria)

본 문서는 Quantum ESPRESSO를 이용한 DFT 계산 시, 계산이 성공적으로 완료되었는지 판단하는 3가지 핵심 기준(Criteria)과 그 과학적 의미를 설명합니다.

---

## 1. 전자 밀도 수렴 (SCF Convergence)
전자의 바닥 상태(Ground State)를 찾기 위한 Self-Consistent Field (SCF) 루프의 종료 조건입니다.

*   **파라미터:** `conv_thr` (Convergence Threshold)
*   **일반적인 기준값:** $1.0 \times 10^{-6}$ ~ $1.0 \times 10^{-8}$ Ry
*   **의미:**
    *   입력 전하 밀도($\rho_{in}$)와 출력 전하 밀도($\rho_{out}$)의 차이(Error)가 이 값보다 작아져야 합니다.
    *   **"Estimated scf accuracy"** 로그가 이 값 밑으로 떨어지면 SCF가 종료됩니다.
*   **참고 문헌:** *Giannozzi et al., J. Phys.: Condens. Matter 21, 395502 (2009).* (QE Main Paper).

## 2. 이온 완화 수렴 (Ionic Convergence / Geometry Optimization)
원자들의 위치를 최적화(`relax`)할 때, 원자들이 평형 위치에 도달했는지 판단하는 기준입니다.

*   **파라미터 1:** `etot_conv_thr` (Energy Threshold)
    *   **기준값:** $1.0 \times 10^{-4}$ Ry
    *   **의미:** 이전 스텝과 현재 스텝의 **총 에너지 차이**가 이 값보다 작아야 합니다. (에너지가 바닥을 쳤는가?)
*   **파라미터 2:** `forc_conv_thr` (Force Threshold)
    *   **기준값:** $1.0 \times 10^{-3}$ Ry/Bohr
    *   **의미:** 모든 원자에 작용하는 **힘(Force)**이 이 값보다 작아야 합니다. (원자가 더 이상 움직일 이유가 없는가?)
*   **판단:** 위 두 조건이 모두 만족되어야 `bfgs` 알고리즘이 종료됩니다.

## 3. 셀 완화 수렴 (Cell Convergence / Variable Cell Relaxation)
셀의 부피와 모양까지 최적화(`vc-relax`)할 때 추가되는 기준입니다.

*   **파라미터:** `press_conv_thr` (Pressure Threshold)
    *   **기준값:** 0.5 kbar (0.5 ~ 1.0 kbar)
    *   **의미:** 시스템 전체에 걸리는 **압력(Stress)**이 목표 압력(보통 0)과 비슷해졌는가?
*   **주의:** `vc-relax`는 Force와 Pressure가 동시에 수렴해야 하므로 가장 까다롭습니다.

---

## 요약 (Summary Checklist)

| 구분 | 파라미터 | 권장값 | 의미 |
| :--- | :--- | :--- | :--- |
| **전자** | `conv_thr` | `1.0d-6` Ry | 전자 밀도 합의 완료 |
| **에너지** | `etot_conv_thr` | `1.0d-4` Ry | 에너지 변화 없음 |
| **힘** | `forc_conv_thr` | `1.0d-3` Ry/Bohr | 원자 이동 멈춤 |
| **압력** | `press_conv_thr` | `0.5` kbar | 셀 크기 고정 |

이 조건들을 모두 만족했을 때 비로소 **"JOB DONE"** 메시지가 출력됩니다.
