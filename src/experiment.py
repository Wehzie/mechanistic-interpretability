"""
Main experiment orchestrator.

Run the full 5-phase steganography experiment pipeline.
"""

import argparse

from .phase0_baseline import run_phase0
from .phase1_prompt_generation import run_phase1
from .phase2_poisoned_helper import run_phase2
from .phase3_decoder import run_phase3
from .phase4_evaluation import run_phase4
from .utils import ensure_results_dir


def run_all_phases(resume: bool = True):
    """Run all phases sequentially."""
    ensure_results_dir()
    
    print("="*60)
    print("STEGANOGRAPHY EXPERIMENT")
    print("="*60)
    print()
    
    print("Phase 0: Baseline Naturalness Measurement")
    print("-" * 60)
    run_phase0(resume=resume)
    print()
    
    print("Phase 1: Malicious Prompt Generation")
    print("-" * 60)
    run_phase1(resume=resume)
    print()
    
    print("Phase 2: Poisoned Helper Execution")
    print("-" * 60)
    run_phase2(resume=resume)
    print()
    
    print("Phase 3: Decoder Execution")
    print("-" * 60)
    run_phase3(resume=resume)
    print()
    
    print("Phase 4: Evaluation and Metrics")
    print("-" * 60)
    run_phase4()
    print()
    
    print("="*60)
    print("EXPERIMENT COMPLETE")
    print("="*60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run steganography experiment phases"
    )
    parser.add_argument(
        "--phase",
        type=int,
        choices=[0, 1, 2, 3, 4],
        help="Run a specific phase (0-4). If not specified, runs all phases.",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Don't resume from existing results (start fresh)",
    )
    
    args = parser.parse_args()
    
    resume = not args.no_resume
    ensure_results_dir()
    
    if args.phase is not None:
        # Run specific phase
        if args.phase == 0:
            run_phase0(resume=resume)
        elif args.phase == 1:
            run_phase1(resume=resume)
        elif args.phase == 2:
            run_phase2(resume=resume)
        elif args.phase == 3:
            run_phase3(resume=resume)
        elif args.phase == 4:
            run_phase4()
    else:
        # Run all phases
        run_all_phases(resume=resume)


if __name__ == "__main__":
    main()

