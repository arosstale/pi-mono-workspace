#!/bin/bash
# Quick MSAM batch export

cd /home/majinbu/msam

python -m msam.remember store "User email: ciao@openclaw.ai"
python -m msam.remember store "User phone: +39 329 348 4956"
python -m msam.remember store "User location: Bergamo, Italia"
python -m msam.remember store "User timezone: UTC"
python -m msam.remember store "User GitHub: https://github.com/arosstale"
python -m msam.remember store "Rayan is CEO and Founder of N-Art AI Trading platform"
python -m msam.remember store "Rayan email: rayan@n-art.io"
python -m msam.remember store "OpenClaw Sales Site: https://openclaw-sales.netlify.app"
python -m msam.remember store "N-Art Sales Site: https://n-art-sales.netlify.app"
python -m msam.remember store "OpenClaw Wrappers Site: https://openclaw-wrappers.vercel.app"
python -m msam.remember store "VibeClaw Site: https://vibeclaw-openclaw.netlify.app"
python -m msam.remember store "OpenClaw workspace: ~/pi-mono-workspace"
python -m msam.remember store "MSAM provides 99.3% token savings (51 vs 7,327 tokens)"
python -m msam.remember store "MSAM has 4 memory streams: semantic, episodic, procedural, working"
python -m msam.remember store "MSAM uses ACT-R activation scoring and confidence-gated retrieval"
python -m msam.remember store "T013: Graceful Degradation > Brittle Perfection"
python -m msam.remember store "T014: The RSI Veto Protocol - RSI > 70 veto for longs"
python -m msam.remember store "T015: The Falling Knife Paradox - Low RSI in downtrend is a trap"
python -m msam.remember store "Git repo: https://github.com/arosstale/pi-mono-workspace"
python -m msam.remember store "Node version: v24.13.1, Shell: bash 5.1.16"
python -m msam.remember store "Trading systems: Quant, nano-agent, SuperQuant, Dalio, Nash"
python -m msam.remember store "Skill location: ~/pi-mono-workspace/skills/"
python -m msam.remember store "Sales sites auto-deploy to Netlify on git push"
python -m msam.remember store "OpenSSH, fail2ban, UFW security hardened"
python -m msam.remember store "User prefers dark mode and concise responses"
python -m msam.remember store "User values speed, execution, revenue and results"
python -m msam.remember store "User dislikes slow deployment and authentication friction"

python -m msam.remember stats
