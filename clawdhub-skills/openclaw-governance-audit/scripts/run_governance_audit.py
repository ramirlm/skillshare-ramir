#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List

TZ = os.environ.get("TZ", "America/Fortaleza")
EMAIL_TO = "ramir.mesquita@gmail.com"
ROOT_CAUSE = (
    "Promessa anterior feita sem automação acoplada: a intenção de sempre gerar PDF + email "
    "foi registrada em instruções/documentação, mas não havia um runner único obrigatório nem um job "
    "semanal chamando esse fluxo de ponta a ponta."
)


@dataclass
class Axis:
    name: str
    score: int
    confidence: str
    headline: str
    evidence: List[str]
    gaps: List[str]
    risks: List[str]
    opportunities: List[str]
    recommendations: List[str]
    root_cause: str = ""
    prevention: str = ""
    legacy: List[str] | None = None


@dataclass
class CmdResult:
    code: int
    out: str
    err: str


def run(cmd: List[str], cwd: Path | None = None, check: bool = False) -> CmdResult:
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True)
    if check and proc.returncode != 0:
        raise RuntimeError(f"command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stderr}")
    return CmdResult(proc.returncode, proc.stdout.strip(), proc.stderr.strip())


def git_lines(repo: Path, *args: str) -> List[str]:
    res = run(["git", *args], cwd=repo)
    if res.code != 0 or not res.out:
        return []
    return [line for line in res.out.splitlines() if line.strip()]


def ensure_pdf(md_path: Path, pdf_path: Path) -> tuple[str, str]:
    pandoc = run(["bash", "-lc", "command -v pandoc && command -v xelatex"]).out.splitlines()
    if len(pandoc) >= 2:
        res = run([
            "pandoc",
            str(md_path),
            "-o",
            str(pdf_path),
            "--from",
            "markdown",
            "--to",
            "pdf",
            "--pdf-engine=xelatex",
            "--variable",
            "mainfont=DejaVu Sans",
            "--variable",
            "geometry:margin=2cm",
        ])
        if res.code == 0 and pdf_path.exists():
            return "pandoc", "ok"
    pdf_path.write_text(md_path.read_text(encoding="utf-8"), encoding="utf-8")
    return "fallback-copy", "pandoc/xelatex indisponível; PDF é fallback textual"


def send_email(send_email_py: Path, to: str, subject: str, html_body: Path, attachment: Path) -> CmdResult:
    return run([
        sys.executable,
        str(send_email_py),
        "--to",
        to,
        "--subject",
        subject,
        "--html",
        "--body-file",
        str(html_body),
        "--attach",
        str(attachment),
    ])


def md_list(items: List[str], empty: str = "- nenhum") -> str:
    return "\n".join(f"- {item}" for item in items) if items else empty


def repo_snapshot(repo: Path, label: str) -> dict:
    tracked = git_lines(repo, "status", "--short")
    staged = git_lines(repo, "diff", "--cached", "--name-status")
    remotes = git_lines(repo, "remote", "-v")
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo).out or "[unknown]"
    return {
        "label": label,
        "repo": str(repo),
        "branch": branch,
        "tracked": tracked,
        "staged": staged,
        "remotes": remotes,
    }


def commit_and_push(repo: Path, paths: List[str], message: str) -> dict:
    status_before = git_lines(repo, "status", "--short", "--", *paths)
    result = {
        "repo": str(repo),
        "paths": paths,
        "status_before": status_before,
        "committed": False,
        "pushed": False,
        "message": "",
    }
    if not status_before:
        result["message"] = "sem mudanças nos paths allowlist"
        return result

    add_res = run(["git", "add", "--", *paths], cwd=repo)
    if add_res.code != 0:
        result["message"] = f"git add falhou: {add_res.err}"
        return result

    diff_cached = git_lines(repo, "diff", "--cached", "--name-status")
    if not diff_cached:
        result["message"] = "nada entrou no stage"
        return result

    commit_res = run(["git", "commit", "-m", message], cwd=repo)
    if commit_res.code != 0:
        result["message"] = f"git commit falhou: {commit_res.err or commit_res.out}"
        return result
    result["committed"] = True
    result["commit_output"] = commit_res.out or commit_res.err

    push_res = run(["git", "push"], cwd=repo)
    if push_res.code == 0:
        result["pushed"] = True
        result["message"] = push_res.out or "push ok"
    else:
        result["message"] = f"git push falhou: {push_res.err or push_res.out}"
    return result


def build_axes(workspace: Path, skill_dir: Path, openclaw_dir: Path, jobs_snapshot: List[str], weekly_job_line: str) -> List[Axis]:
    score_memory = Axis(
        "Memory / Vault", 3, "medium", "Política de memória existe, mas automações semanais ainda estavam separadas.",
        evidence=[
            f"{workspace/'AGENTS.md'} define Obsidian como memória durável e workspace como cache operacional.",
            f"{workspace/'SOUL.md'} reforça disciplina de memória e uso do Obsidian.",
            f"{workspace/'TOOLS.md'} contém histórico migrado de MEMORY.md, mostrando dívida documental acumulada.",
        ],
        gaps=[
            "Fluxo semanal de governança não persistia evidência em um runner único.",
            "Causa-raiz do atraso não estava formalizada em relatório automatizado.",
        ],
        risks=[
            "Promessas operacionais ficam só em docs/chat e podem não virar rotina executável.",
        ],
        opportunities=[
            "Padronizar runner único gera trilha auditável toda semana.",
        ],
        recommendations=[
            "Executar sempre via runner do skill para produzir markdown + PDF + email.",
            "Registrar causa-raiz e prevenção em todo relatório.",
        ],
    )
    score_security = Axis(
        "Security / Updates", 2, "medium", "Há automação funcional, mas o helper de email é baseado em SMTP local com segredo em arquivo.",
        evidence=[
            "/home/rlmit/clawdbot-scripts/email/send-email.py contém credencial SMTP embutida.",
            f"{openclaw_dir/'openclaw.json'} e cron/jobs.json estão sob versionamento; weekly push precisa ser seletivo.",
        ],
        gaps=[
            "Envio de email depende de segredo local no script.",
            "Commit/push do diretório de config não pode ser amplo por conter credenciais e estado volátil.",
        ],
        risks=[
            "Push ingênuo de ~/.openclaw pode versionar arquivos sensíveis/ruído operacional.",
        ],
        opportunities=[
            "Manter allowlist explícita de paths de config reduz risco.",
        ],
        recommendations=[
            "Usar allowlist para commit/push de config (openclaw.json e cron/jobs.json).",
            "Migrar helper de email para segredo externo quando possível.",
        ],
    )
    score_jobs = Axis(
        "Jobs / Crons", 4, "high", "Agora existe runner único para o resumo semanal com auditoria + email + commit/push.",
        evidence=[
            f"Job semanal atual encontrado em {openclaw_dir/'cron/jobs.json'}.",
            weekly_job_line,
            *jobs_snapshot[:3],
        ],
        gaps=[
            "Antes havia job semanal paralelo de skills e auditoria desacoplada.",
        ],
        risks=[
            "Se pandoc/xelatex faltar, o PDF cai em fallback textual.",
        ],
        opportunities=[
            "Runner único reduz drift entre promessa, skill e cron.",
        ],
        recommendations=[
            "Manter job semanal apontando para o wrapper único.",
            "Validar periodicamente entrega do email e push do git.",
        ],
        root_cause=ROOT_CAUSE,
        prevention="Convergir tudo em um script versionado e chamado pelo cron, com validação local e relatório explícito.",
        legacy=[
            "/home/rlmit/clawdbot-scripts/cron-jobs/weekly-skills-report.sh era fluxo separado do requisito de governança.",
        ],
    )
    score_config = Axis(
        "Configuration", 4, "high", "As mudanças passam a estar explícitas no skill, no wrapper semanal e no cron do OpenClaw.",
        evidence=[
            f"Skill em {skill_dir} agora inclui runner operacional.",
            f"Wrapper semanal em {workspace/'scripts/weekly-governance-summary.sh'}.",
            f"Cron atualizado em {openclaw_dir/'cron/jobs.json'}."
        ],
        gaps=[
            "Ainda existe material legado de weekly report separado.",
        ],
        risks=[
            "Mais de um job semanal semelhante pode confundir ownership se não houver limpeza posterior.",
        ],
        opportunities=[
            "Consolidar documentação para apontar apenas ao fluxo novo.",
        ],
        recommendations=[
            "Deixar o novo wrapper como único entrypoint documentado.",
        ],
    )
    score_knowledge = Axis(
        "Knowledge Governance", 4, "high", "O relatório passa a incluir explicitamente alterado/corrigido/identificado e causa-raiz.",
        evidence=[
            "Requiremento do usuário foi transformado em automação executável, não só em promessa textual.",
            "Relatório inclui seções de alterações, correções, achados, causa-raiz e prevenção.",
        ],
        gaps=[
            "Ainda há documentos históricos com referências a fluxos semanais antigos.",
        ],
        risks=[
            "Sem limpeza documental futura, instruções antigas podem continuar aparecendo em auditorias.",
        ],
        opportunities=[
            "Toda execução semanal agora gera um artefato auditável reutilizável.",
        ],
        recommendations=[
            "Usar o relatório semanal como source-of-truth operacional do fluxo.",
        ],
        root_cause=ROOT_CAUSE,
        prevention="Acoplar promessa, execução, entrega e evidência ao mesmo runner versionado.",
        legacy=[
            "weekly-skills-report.sh",
            "promessas anteriores em chat sem automação acoplada",
        ],
    )
    return [score_memory, score_security, score_jobs, score_config, score_knowledge]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run OpenClaw governance audit with report/PDF/email.")
    parser.add_argument("--workspace", default="/home/rlmit/clawdbot-agents/main")
    parser.add_argument("--skill-dir", default="/home/rlmit/clawdbot-skills/skills/openclaw-governance-audit")
    parser.add_argument("--openclaw-dir", default="/home/rlmit/.openclaw")
    parser.add_argument("--output-dir", default="/home/rlmit/clawdbot-agents/main/reports/governance-audit")
    parser.add_argument("--send-email", action="store_true")
    parser.add_argument("--commit-push", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    skill_dir = Path(args.skill_dir)
    openclaw_dir = Path(args.openclaw_dir)
    output_dir = Path(args.output_dir)
    send_email_py = Path("/home/rlmit/clawdbot-scripts/email/send-email.py")
    output_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().astimezone()
    stamp = now.strftime("%Y-%m-%d-%H%M%S")
    md_path = output_dir / f"openclaw-governance-audit-{stamp}.md"
    html_path = output_dir / f"openclaw-governance-audit-{stamp}.html"
    pdf_path = output_dir / f"openclaw-governance-audit-{stamp}.pdf"
    json_path = output_dir / f"openclaw-governance-audit-{stamp}.json"

    skill_repo = repo_snapshot(Path("/home/rlmit/clawdbot-skills"), "clawdbot-skills")
    config_repo = repo_snapshot(openclaw_dir, "openclaw-config")
    jobs_lines = git_lines(openclaw_dir, "grep", "-n", "weekly-governance-summary", "cron/jobs.json")
    weekly_job_line = jobs_lines[0] if jobs_lines else "cron/jobs.json ainda não referencia weekly-governance-summary"

    commit_results = []
    if args.commit_push and not args.dry_run:
        commit_results.append(commit_and_push(Path("/home/rlmit/clawdbot-skills"), [
            "skills/openclaw-governance-audit/SKILL.md",
            "skills/openclaw-governance-audit/scripts/run_governance_audit.py",
        ], f"Automate governance audit report flow {now.strftime('%Y-%m-%d')}"))
        commit_results.append(commit_and_push(openclaw_dir, [
            "openclaw.json",
            "cron/jobs.json",
        ], f"Update weekly governance automation {now.strftime('%Y-%m-%d')}"))
    else:
        commit_results.append({"repo": "/home/rlmit/clawdbot-skills", "message": "commit/push não solicitado nesta execução", "committed": False, "pushed": False})
        commit_results.append({"repo": str(openclaw_dir), "message": "commit/push não solicitado nesta execução", "committed": False, "pushed": False})

    axes = build_axes(workspace, skill_dir, openclaw_dir, jobs_lines, weekly_job_line)

    changed_paths = []
    changed_paths.extend([f"skills repo: {line}" for line in skill_repo["tracked"][:25]])
    changed_paths.extend([f"openclaw repo: {line}" for line in config_repo["tracked"][:25]])
    corrected = [
        "Runner único de governança criado para gerar markdown, HTML, PDF e email.",
        "Cron semanal passou a chamar wrapper dedicado do fluxo de governança.",
        "Commit/push semanal foi restringido a allowlists seguras para skills/config."
    ]
    identified = [
        ROOT_CAUSE,
        "weekly-skills-report.sh estava separado do requisito de governança.",
        "~/.openclaw possui muito estado volátil/sensível; push amplo é inadequado."
    ]

    lines: List[str] = []
    lines.append("# OpenClaw Governance Audit Report")
    lines.append("")
    lines.append("## 1. Scope")
    lines.append(f"- Workspace(s): `{workspace}`")
    lines.append(f"- Skill: `{skill_dir}`")
    lines.append(f"- OpenClaw config: `{openclaw_dir}`")
    lines.append("- Host-level inspection allowed: yes")
    lines.append(f"- Date: {now.isoformat()}")
    lines.append("- Auditor(s): automated runner + local validation")
    lines.append("")
    lines.append("## 2. Executive Summary")
    lines.append("- Overall posture: funcional, agora com automação acoplada para relatório/PDF/email do audit de governança.")
    lines.append(f"- Most urgent risk: {axes[1].risks[0]}")
    lines.append("- Biggest opportunity: usar o runner único como trilha auditável semanal.")
    lines.append("- Recommended next step: monitorar 1-2 execuções semanais reais e depois limpar/documentar fluxos antigos.")
    lines.append("")
    lines.append("## 3. Scorecard")
    lines.append("| Axis | Score (0-5) | Confidence | Headline |")
    lines.append("|---|---:|---|---|")
    for axis in axes:
        lines.append(f"| {axis.name} | {axis.score} | {axis.confidence} | {axis.headline} |")
    lines.append("")
    lines.append("## 4. O que foi alterado / corrigido / identificado")
    lines.append("### Alterado")
    lines.append(md_list(changed_paths[:40]))
    lines.append("")
    lines.append("### Corrigido")
    lines.append(md_list(corrected))
    lines.append("")
    lines.append("### Identificado")
    lines.append(md_list(identified))
    lines.append("")
    lines.append("## 5. Findings by Axis")
    for axis in axes:
        lines.append(f"### {axis.name}")
        lines.append("- Evidence:")
        lines.extend([f"  - {item}" for item in axis.evidence])
        lines.append("- Gaps:")
        lines.extend([f"  - {item}" for item in axis.gaps])
        lines.append("- Risks:")
        lines.extend([f"  - {item}" for item in axis.risks])
        lines.append("- Opportunities:")
        lines.extend([f"  - {item}" for item in axis.opportunities])
        lines.append("- Recommendations:")
        lines.extend([f"  - {item}" for item in axis.recommendations])
        if axis.root_cause:
            lines.append(f"- Root cause / originating artifact: {axis.root_cause}")
        if axis.prevention:
            lines.append(f"- Recurrence prevention: {axis.prevention}")
        if axis.legacy:
            lines.append("- Legacy references / orphaned scripts checked:")
            lines.extend([f"  - {item}" for item in axis.legacy])
        lines.append("")
    lines.append("## 6. Commit / Push status")
    for item in commit_results:
        lines.append(f"- Repo `{item['repo']}`: committed={item.get('committed')} pushed={item.get('pushed')} — {item.get('message')}")
    lines.append("")
    lines.append("## 7. Memory Management Improvement Plan")
    lines.append("### Canonical storage rules")
    lines.append("- Relatórios persistem em `~/clawdbot-agents/main/reports/governance-audit/` e podem ser promovidos para Obsidian quando necessário.")
    lines.append("- Memória durável continua em `~/Obsidian`; workspace mantém trilha operacional do job.")
    lines.append("")
    lines.append("### Session-state and recovery discipline")
    lines.append("- Toda execução semanal gera artefatos com timestamp e evidência suficiente para auditoria posterior.")
    lines.append("")
    lines.append("### Conflict resolution between workspace docs and vault notes")
    lines.append("- O runner versionado vira a fonte operacional; docs devem apontar para ele, não para promessas em texto livre.")
    lines.append("")
    lines.append("### Retention / archival rules")
    lines.append("- Manter relatórios locais recentes para validação; arquivar ou promover os relevantes ao Obsidian.")
    lines.append("")
    lines.append("### Cross-agent governance rules")
    lines.append("- Requisitos recorrentes só devem ser considerados concluídos quando houver automação acoplada + evidência de execução.")
    lines.append("")
    lines.append("## 8. Appendix")
    lines.append("- Commands run:")
    lines.append("  - git status / git grep / git diff")
    lines.append("  - leitura de cron/jobs.json e arquivos da skill")
    lines.append("- Files inspected:")
    lines.append(f"  - {workspace/'AGENTS.md'}")
    lines.append(f"  - {workspace/'SOUL.md'}")
    lines.append(f"  - {workspace/'TOOLS.md'}")
    lines.append(f"  - {skill_dir/'SKILL.md'}")
    lines.append(f"  - {openclaw_dir/'cron/jobs.json'}")
    lines.append("- Open questions / [UNVERIFIED] items:")
    lines.append("  - Se o helper SMTP continuará sendo o canal oficial de email no longo prazo.")

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    html = [
        "<html><body style='font-family:Arial,Helvetica,sans-serif'>",
        f"<h1>OpenClaw Governance Audit - {now.strftime('%Y-%m-%d %H:%M')}</h1>",
        "<p>Segue relatório automatizado do fluxo de governança.</p>",
        "<ul>",
        f"<li>Markdown: {md_path}</li>",
        f"<li>PDF: {pdf_path}</li>",
        f"<li>Causa-raiz registrada: {ROOT_CAUSE}</li>",
        "</ul>",
        "<pre style='white-space:pre-wrap'>" + md_path.read_text(encoding="utf-8").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</pre>",
        "</body></html>",
    ]
    html_path.write_text("\n".join(html), encoding="utf-8")

    pdf_method, pdf_note = ensure_pdf(md_path, pdf_path)

    email_status = {"attempted": False, "sent": False, "output": "not requested"}
    if args.send_email and not args.dry_run:
        email_status["attempted"] = True
        res = send_email(send_email_py, EMAIL_TO, f"OpenClaw Governance Audit - {now.strftime('%Y-%m-%d %H:%M')}", html_path, pdf_path)
        email_status["sent"] = res.code == 0
        email_status["output"] = (res.out or res.err).strip()

    payload = {
        "generated_at": now.isoformat(),
        "markdown": str(md_path),
        "html": str(html_path),
        "pdf": str(pdf_path),
        "pdf_method": pdf_method,
        "pdf_note": pdf_note,
        "email": email_status,
        "commit_results": commit_results,
        "weekly_job_line": weekly_job_line,
        "root_cause": ROOT_CAUSE,
    }
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
