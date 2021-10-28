*** 
## 1.Installation
- recommand OS: **Ubuntu 18.04**
- install ***JDK (1.8)*** for the usage of ***ULTIMATE***
	- sudo add-apt-repository ppa:openjdk-r/ppa
	- sudo apt install openjdk-8-jre-headless
	- sudo apt install openjdk-8-jdk-headless
- install python package

 	-- if Ubuntu18.04: ```sudo apt-get install python3-pip```
 	
	-- for turtle: ```sudo apt-get install python3-tk```

	```
	pip3 install turtle, numpy, tarjan, openpyxl
	```
- create a new folder as ***$ROOT***
	- ``` cd $ROOT ```
	- ``` git clone git@github.com:Verifier4UP/Trace-Refinement-based-Verification.git ```
	- |-- **Trace-Refinement-based-Verification**<br/>
		&emsp; &emsp; &emsp;|-- **ArtifactBenchmark** <br/>
		&emsp; &emsp; &emsp;|-- **[cloc](https://github.com/AlDanial/cloc)** <br/>
		&emsp; &emsp; &emsp;|-- **demo** <br/>
		&emsp; &emsp; &emsp;|-- **[UAutomizer-linux](https://github.com/ultimate-pa/ultimate/releases) (v0.1.25)** <br/>
		&emsp; &emsp; &emsp;|-- **Verifier4UP** <br/>
	- modify the configuration in **./Trace-Refinement-based-Verification/env_setup.py**
	- modify .bashrc 
		- export PYTHONPATH="\$ROOT/Trace-Refinement-based-Verification:$PYTHONPATH"

***
## 2. Benchmark

|--**ArtifactBenchmark**<br/>
		&emsp; &emsp; &emsp;|-- **benchmark** - for ***experiment1*** <br/>
		&emsp; &emsp; &emsp;|-- **svcomp** - for ***experiment2*** <br/>


***
## 3.Usage
	
```
cd $ROOT/Trace-Refinement-based-Verification/demo
```
- prepare the boogie program to be verified in **./demo/example** like ***demo.bpl***
- **Ours:** ``` python3 Ours.py demo.bpl ```

	After a few seconds, when the command finishes, you can view the following result：

	```
	step: separating program into coh/non-coh...
	Mode: auto
	-- query time:  0.005437135696411133
	coherent:  ['./coherence_0.ats']
	non-coherent:  ['./noncoherence_0.ats']
	++ seperation time: 0.006s.
	finished.


	step: Verification & Trace Refinement...
	----------------------------------------
		        Verification: 
	./coherence_0.ats is verified to be correct

	++ verification time:  0.001s.
	----------------------------------------
		        Trace Refinement: 
	-- generalization time:  0.10810065269470215
	-- check empty time:  0.005762815475463867
	congratulation! it takes 4 refinements.
	./noncoherence_0.ats is checked to be correct

	++ trace refinement time:  0.183s.
	----------------------------------------
	finished.


	----------------------------------------
	----------------------------------------
	The program is verified/checked to be correct
	the whole process takes 1.263s.

	```
	It means our method splits the program into a coherent sub-program and a non-coherent sub-program, then does the congruence-based verification and the congruence-based trace abstraction, respectively. The final result shows our method takes 1.263s to verify the program to be correct.
- **ULTIMATE:** ``` python3 UAutomizer.py demo.bpl ```

	After a few seconds, when the command finishes, you can view the following result：

	```
	 --- Results ---
	 * Results from de.uni_freiburg.informatik.ultimate.core:
	  - StatisticsResult: Toolchain Benchmarks
	    Benchmark results are:
	 * Boogie PL CUP Parser took 0.16 ms. Allocated memory is still 514.9 MB. Free memory is still 480.4 MB. There was no memory consumed. Max. memory is 11.5 GB.
	 * Boogie Preprocessor took 42.04 ms. Allocated memory is still 514.9 MB. Free memory was 480.4 MB in the beginning and 477.7 MB in the end (delta: 2.7 MB). Peak memory consumption was 2.7 MB. Max. memory is 11.5 GB.
	 * RCFGBuilder took 225.23 ms. Allocated memory is still 514.9 MB. Free memory was 477.7 MB in the beginning and 466.8 MB in the end (delta: 10.9 MB). Peak memory consumption was 10.9 MB. Max. memory is 11.5 GB.
	 * TraceAbstraction took 386.67 ms. Allocated memory is still 514.9 MB. Free memory was 466.8 MB in the beginning and 447.9 MB in the end (delta: 18.9 MB). Peak memory consumption was 18.9 MB. Max. memory is 11.5 GB.
	 * Results from de.uni_freiburg.informatik.ultimate.plugins.generator.traceabstraction:
	  - PositiveResult [Line: 23]: assertion always holds
	    For all program executions holds that assertion always holds at this location
	  - AllSpecificationsHoldResult: All specifications hold
	    1 specifications checked. All of them hold
	  - StatisticsResult: Ultimate Automizer benchmark data
	    CFG has 1 procedures, 6 locations, 1 error locations. Result: SAFE, OverallTime: 0.3s, OverallIterations: 1, TraceHistogramMax: 1, AutomataDifference: 0.0s, DeadEndRemovalTime: 0.0s, HoareAnnotationTime: 0.0s, HoareTripleCheckerStatistics: 3 SDtfs, 3 SDslu, 0 SDs, 0 SdLazy, 3 SolverSat, 2 SolverUnsat, 0 SolverUnknown, 0 SolverNotchecked, 0.0s Time, PredicateUnifierStatistics: 0 DeclaredPredicates, 2 GetRequests, 1 SyntacticMatches, 0 SemanticMatches, 1 ConstructedPredicates, 0 IntricatePredicates, 0 DeprecatedPredicates, 0 ImplicationChecksByTransitivity, 0.0s Time, 0.0s BasicInterpolantAutomatonTime, BiggestAbstraction: size=6occurred in iteration=0, traceCheckStatistics: No data available, InterpolantConsolidationStatistics: No data available, PathInvariantsStatistics: No data available, 0/0 InterpolantCoveringCapability, TotalInterpolationStatistics: No data available, 0.0s DumpTime, AutomataMinimizationStatistics: 0.0s AutomataMinimizationTime, 1 MinimizatonAttempts, 0 StatesRemovedByMinimization, 0 NontrivialMinimizations, HoareAnnotationStatistics: No data available, RefinementEngineStatistics: TRACE_CHECK: 0.0s SsaConstructionTime, 0.0s SatisfiabilityAnalysisTime, 0.0s InterpolantComputationTime, 3 NumberOfCodeBlocks, 3 NumberOfCodeBlocksAsserted, 1 NumberOfCheckSat, 2 ConstructedInterpolants, 0 QuantifiedInterpolants, 8 SizeOfPredicates, 1 NumberOfNonLiveVariables, 8 ConjunctsInSsa, 3 ConjunctsInUnsatCore, 1 InterpolantComputations, 1 PerfectInterpolantSequences, 0/0 InterpolantCoveringCapability, INVARIANT_SYNTHESIS: No data available, INTERPOLANT_CONSOLIDATION: No data available, ABSTRACT_INTERPRETATION: No data available, PDR: No data available, SIFA: No data available, ReuseStatistics: No data available
	RESULT: Ultimate proved your program to be correct!
	TIMECOST: 4.020611763000488


	----------------------------------------
	----------------------------------------
	The program is verified/checked to be correct
	the whole process takes 4.021s in 2 refinements.
	```
	
	It means ULTIMATE takes 2 iterations to do the trace refinement. And the final result shows ULTIMATE takes 4.021s to verify the program to be correct.


***
## 4.Experimental Reproduction
```
cd $ROOT/Trace-Refinement-based-Verification/Verifier4UP/src/RunExperiment
```

### 4.1 benchmark 1

> The generation-related code can be found at $ROOT/Trace-Refinement-based-Verification/Verifier4UP/src/ProgramGenerator

Use the following command to reproduce the result of the first task in the paper. (It takes around **4 hours**)

```
./Run_benchmark.sh
```
When the command finishes, you can view the following result：

```
There are total 50 programs.
UAutomizer: timeout-16  better-11
Ours: timeout-0 better-39
for both succeed program(34), UAutomizer is better(11), Ours is better(23)
and the speed_ratio is  3.6124634162184024(34)
```
In the total 50 programs, our prototype completes the verification tasks of 50 programs (100%), while ULTIMATE completes the verification of 34 programs (68%), which indicates the effectiveness of our method. For the 34 programs that can be verified by both our method and ULTIMATE, our method performed better on 23 programs (67.6%). On average, our method achieves 3.6x speedups for the verified programs.

### 4.2 benchmark 2

> Each selected C programs and its uninterpreted version are available at $ROOT/Trace-Refinement-based-Verification/ArtifactBenchmark

Use the following command to reproduce the result of the second task in the paper. (It takes around **10 mins**)

```
./Run_svcomp.sh
```
When the command finishes, you can view the following result：

```
There are total 46 programs.
UAutomizer: timeout-0  better-2
Ours: timeout-0 better-44
for both succeed program(46), UAutomizer is better(2), Ours is better(44)
and the speed_ratio is  1.9040962586426589(46)
and co_speed_ratio is  2.130457750215989(29)
and nco_speed_ratio is  1.5179501847822725(17)

```
In the total 46 programs, our method performs better on 44 programs (95.7%) than ULTIMATE. On average, our method achieves 1.90x speedups. Besides, for the 29 coherent programs, our method can achieve 2.13x speedups on average; for the remaining 17 non-coherent programs, our method achieves 1.52x speedups on average. 

|  Coherent ones   | Non-coherent ones  |
|  ----  | ----  |
|  array\_1-1, array\_1-2, array\_3-1, array\_3-2, <br> array3, bin-suffix-5, const\_1-1, const\_1-2, <br> count\_by\_1(2), diamond\_2-2, eq2, even(2), <br> functions\_1-1, functions\_1-2, gj2007(2), <br> hhk2008(2), Mono4\_1(2), multivar\_1-1, <br> simple\_1-1, simple\_1-2, simple\_2-1, simple\_2-2, <br> while\_infinite\_loop\_1,  while\_infinite\_loop\_2 | array\_2-1, bhmr2007, const, diamond\_1-2, eq1, <br> in-de20, jm2006, mod3, Mono1\_1-2, multivar\_1-2, <br> nested\_1-1, nested\_1-2, simple\_vardep\_2, <br> underapprox\_1-1, underapprox\_1-2, <br> underapprox\_2-1, underapprox\_2-2 |


***
## Contacts
Please feel free to contact us if you have any problem.

* Verifier4UP@outlook.com
