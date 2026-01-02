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


def run_all_phases(resume: bool = True, test_mode: bool = False, use_flex: bool = False):
    """Run all phases sequentially."""
    ensure_results_dir()
    
    print("="*60)
    if test_mode:
        print("STEGANOGRAPHY EXPERIMENT (TEST MODE)")
    else:
        print("STEGANOGRAPHY EXPERIMENT")
    print("="*60)
    if test_mode:
        print("⚠️  TEST MODE: Reduced API calls for minimal expenses")
    if use_flex:
        print("⚡ FLEX MODE: Using flex processing with extended timeout (15 minutes)")
    print()
    
    print("Phase 0: Baseline Naturalness Measurement")
    print("-" * 60)
    run_phase0(resume=resume, test_mode=test_mode, use_flex=use_flex)
    print()
    
    print("Phase 1: Malicious Prompt Generation")
    print("-" * 60)
    run_phase1(resume=resume, test_mode=test_mode, use_flex=use_flex)
    print()
    
    print("Phase 2: Poisoned Helper Execution")
    print("-" * 60)
    run_phase2(resume=resume, test_mode=test_mode, use_flex=use_flex)
    print()
    
    print("Phase 3: Decoder Execution")
    print("-" * 60)
    run_phase3(resume=resume, test_mode=test_mode, use_flex=use_flex)
    print()
    
    print("Phase 4: Evaluation and Metrics")
    print("-" * 60)
    run_phase4(test_mode=test_mode)
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
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode with reduced API calls for minimal expenses",
    )
    parser.add_argument(
        "--flex",
        action="store_true",
        help="Enable flex processing mode with extended timeout (15 minutes) and service_tier='flex'",
    )
    
    args = parser.parse_args()
    
    resume = not args.no_resume
    test_mode = args.test_mode
    use_flex = args.flex
    ensure_results_dir()
    
    if args.phase is not None:
        # Run specific phase
        if args.phase == 0:
            run_phase0(resume=resume, test_mode=test_mode, use_flex=use_flex)
        elif args.phase == 1:
            run_phase1(resume=resume, test_mode=test_mode, use_flex=use_flex)
        elif args.phase == 2:
            run_phase2(resume=resume, test_mode=test_mode, use_flex=use_flex)
        elif args.phase == 3:
            run_phase3(resume=resume, test_mode=test_mode, use_flex=use_flex)
        elif args.phase == 4:
            run_phase4(test_mode=test_mode)
    else:
        # Run all phases
        run_all_phases(resume=resume, test_mode=test_mode, use_flex=use_flex)


if __name__ == "__main__":
    main()

