# Theory: decision validity and unavoidable costs

All statements concern a frozen score vector. They do not estimate future model generations or a population of future questions. Proofs below are self-contained; the confidence-sequence construction is an application of established results, not a novelty claim.

## 1. Decision problem

Let d=(d_1,...,d_N) belong to [-1,1]^N and let delta=N^{-1} sum_i d_i. Fix epsilon in [0,1) before examining target scores. The mutually exclusive labels are A if delta>epsilon, E if -epsilon<=delta<=epsilon, and B if delta<-epsilon. Evaluating an item reveals both model scores and therefore its difference. Known positive costs c_i refer to that pair-item evaluation. An algorithm may adaptively choose unseen items using earlier observations, metadata, and independent randomization. It must terminate by N and return one label.

Uniform alpha correctness means that, for every allowed frozen vector d, the probability of a wrong final label is at most alpha. Randomness is that of the evaluation design. A budget-limited unresolved result must be reported as unresolved, rather than E. Defining A by delta>0 instead would overlap with E; this document uses practical superiority to obtain a partition.

## 2. Existing confidence sequences yield valid three-way decisions

**Proposition 1.** Suppose C_t is a (1-alpha) confidence sequence for delta: P_d(delta belongs to C_t for every t)>=1-alpha. Stop the first time the nonempty C_t is contained in one label region, or evaluate the full benchmark and return its exact label. Then the final label is uniformly alpha-correct.

**Proof.** On the simultaneous coverage event, the true delta belongs to the region containing C_t, so every certified label is correct. At census, the vector and its label are known exactly. Hence every wrong decision is contained in the CS failure event. No separate three-way Bonferroni correction is necessary. Empty sets do not yield a certificate. QED.

The same event permits multiple predeclared margins or inspecting all margins after sampling, as statements about this same fixed delta. It does not license selecting a new model pair without additional multiplicity control.

## 3. Without-replacement empirical-Bernstein construction

Set x_i=(d_i+1)/2, mu=(delta+1)/2. Observe a uniformly random permutation X_1,...,X_N. Write S_{t-1}=sum_{j<t} X_j, R_t=N-t+1, and m_t=(N mu-S_{t-1})/R_t. Conditional on the revealed prefix, E[X_t|F_{t-1}]=m_t. Let p_t in [0,1] be any predictable prediction, and choose predictable lambda_t in (0,1). Define psi(lambda)=-log(1-lambda)-lambda.

**Lemma 2.** For each sign s in {-1,+1},

M_t^s = exp(sum_{j<=t} [s lambda_j (X_j-m_j) - psi(lambda_j)(X_j-p_j)^2])

is a nonnegative supermartingale starting at one.

**Proof.** For y in [-1,1] and 0<lambda<1,

exp(lambda y-psi(lambda)y^2)<=1+lambda y.

To verify this, expand lambda y-log(1+lambda y)=sum_{k>=2} (-1)^k(lambda y)^k/k. For y>=0 this is bounded by y^2 sum_{k>=2}lambda^k/k; for y<0 all terms are positive and |y|^k<=y^2. The series is absolutely convergent. Apply the inequality with y=s(X_t-p_t), take conditional expectations, and multiply by exp(s lambda_t(p_t-m_t)). The result is exp(-u)(1+u)<=1, where u=s lambda_t(m_t-p_t)>-1. Multiplication over time proves the claim. QED.

Let A_t=sum_{j<=t}lambda_j N/R_j, Z_t=sum_{j<=t}lambda_j(X_j+S_{j-1}/R_j), and V_t=sum_{j<=t}psi(lambda_j)(X_j-p_j)^2. Ville's inequality for both signs gives the CS

[ (Z_t-log(2/alpha)-V_t)/A_t, (Z_t+log(2/alpha)+V_t)/A_t ].

Transform by 2mu-1 for delta. This is the Waudby-Smith–Ramdas empirical-Bernstein WoR form. Our grid implementation intersects eight constant-lambda CSs with alpha/8 each; the predictable version uses a past-only variance proxy. Hoeffding replaces the variance penalty by sum lambda_j^2/8. These are alternative valid constructions, not optimized universal choices.

Intersecting intervals over earlier times preserves coverage. So does intersecting with the deterministic completion interval [S_t/N,(S_t+N-t)/N]. At full observation the exact mean overrides any earlier empty intersection. The numerical implementation pads bounds outward by 1e-12; the mathematical guarantee is for real arithmetic, not a formally verified floating-point implementation.

## 4. Adaptive stratification

Partition items into H fixed nonempty strata with weights w_h=N_h/N. Construct an alpha_h CS [L_{h,n},U_{h,n}] from a uniform random permutation within each stratum, with sum_h alpha_h<=alpha. Adaptively select a stratum using past revealed data, and reveal its next item. Then

[sum_h w_h L_{h,n_h(t)}, sum_h w_h U_{h,n_h(t)}]

is a (1-alpha) CS for delta, using [-1,1] at a zero count.

**Proof.** The union bound gives simultaneous coverage at every local sample count in every stratum. On that event, weighting the covered stratum means gives coverage at every global time, whatever predictable interleaving was used. Thus Proposition 1 applies. QED.

This is the standard combined-stratum-CS approach. It can be conservative; it does not establish the optimality of the empirical-Neyman allocation or a general advantage of stratification. Stronger union-intersection tests already exist.

## 5. A general indistinguishability lower bound

**Theorem 3 (inclusion constraints).** Fix alpha<1/2 and an algorithm uniformly alpha-correct on a class of frozen vectors. Suppose d and d' in this class have different labels and differ only on a set J. Let Q denote the set queried before termination under d. Then

P_d(Q intersects J)>=1-2alpha.

**Proof.** Couple the algorithm's randomization on the two vectors, holding metadata and any side information identical. Until an item in J is queried, the two observation histories, actions, and stopping decisions coincide. The event of terminating without querying J consequently has the same coupled path on both instances. On every such path the common output is wrong on at least one of d,d', because their correct labels differ. Thus P_d(Q avoids J)<=P_d(error)+P_{d'}(error)<=2alpha. QED.

This argument allows arbitrary adaptive, unequal-probability selection. It requires that the two constructed vectors remain admissible given side information; it cannot be applied if external information has already revealed their difference.

**Corollary 3.1 (cost at a boundary).** Suppose delta=epsilon. Let I={i:d_i<1}, and assume all vectors obtained by increasing one such coordinate to one are allowed. Then

E_d[sum_{i in Q} c_i] >= (1-2alpha) sum_{i in I} c_i.

**Proof.** Each single-coordinate change strictly increases the mean beyond epsilon and changes E to A. Apply Theorem 3 to each singleton and sum c_i P_d(i in Q). QED.

For a constant vector d_i=epsilon<1 and unit costs the bound is (1-2alpha)N. At alpha=.05, any uniformly valid method must evaluate at least 90% in expectation on that instance. For ternary paired binary scores at delta=epsilon and disagreement q, the same bound is (1-2alpha)N[1-(q+epsilon)/2]. The negative boundary is symmetric, replacing d_i<1 by d_i>-1.

More generally, if delta<epsilon, singleton constraints apply whenever (1-d_i)/N>epsilon-delta. Thus near-boundary obstructions depend on the attainable contribution of one unseen item, not solely on variance.

## 6. Homogeneous populations away from a boundary

**Theorem 4 (hidden exceptional items).** Let d_i=b for every i, where -epsilon<=b<=epsilon and b<1. Choose an integer 1<=k<=N satisfying b+k(1-b)/N>epsilon, and suppose every vector formed by setting any k entries to one is admissible. Then

E_b[tau] >= (N-k+1) [1-(2alpha)^(1/k)].

**Proof.** Apply Theorem 3 to each k-subset J and average uniformly over all such subsets, independently of the algorithm. Conditional on the realized queried set of size tau, the fraction of k-subsets avoided is f(tau)=choose(N-tau,k)/choose(N,k), with zero if N-tau<k. Therefore E_b f(tau)<=2alpha. For integer t,

f(t)>=max(1-t/(N-k+1),0)^k,

because each factor (N-t-j)/(N-j) for j=0,...,k-1 is at least 1-t/(N-k+1) when the latter is nonnegative. The right-hand function is convex in real t for integer k>=1. Jensen's inequality then yields max(1-E tau/(N-k+1),0)^k<=2alpha, which rearranges to the result. QED.

At b=epsilon choose k=1 to recover 90% at alpha=.05. At b=0, fixed positive epsilon and large N, k is about N epsilon and the lower bound is of order log(1/alpha)/epsilon. This illustrates why zero observed variance does not justify immediate equivalence certification. These are elementary coupling consequences; no novelty priority is asserted for their finite-benchmark formulation. They are not asserted to be minimax-sharp away from the boundary.

## 7. Distance-dependent consequences and limits

### Distance-dependent extension: nonconstant populations on either side

Let g=||delta|-epsilon|. Choose a nearest decision boundary and the direction toward a different label: increase scores toward +1 for delta<-epsilon or 0<=delta<=epsilon, and decrease scores toward -1 for delta>epsilon or -epsilon<=delta<0. The available change of coordinate i is a_i=1-d_i in the increasing direction and a_i=1+d_i in the decreasing direction. Fix h>0 and let I_h={i:a_i>=h}, M=|I_h|. Put k=floor(Ng/h)+1. Suppose k<=M and replacing any k coordinates of I_h by their directional endpoints is admissible given the side information. Then every uniformly alpha-correct procedure satisfies

E_d[|Q intersect I_h|] >= (M-k+1)[1-(2alpha)^(1/k)],

and therefore E_d[tau] is at least the same quantity. With unequal costs, multiply this bound by min_{i in I_h} c_i, and maximize over admissible h. Singleton constraints can give the stronger sum-of-costs form when k=1.

**Proof.** Every such k-subset permits a mean change of at least kh/N>g and hence changes the label. (Starting in an outer region, overshooting to the opposite outer region still changes the original label.) Apply the inclusion constraint to every k-subset and average. Conditional on Q, the fraction of subsets avoided is choose(M-|Q intersect I_h|,k)/choose(M,k). The convex lower bound and Jensen argument of Section 6 apply with M in place of N. QED.

The strict kh>Ng condition is sufficient on both sides and avoids endpoint-convention ambiguity; it can lose one edit when landing exactly on a closed equivalence endpoint suffices. At g<h/N, k=1 gives E tau >=(1-2alpha)M. This describes a finite-resolution obstruction for heterogeneous vectors and both sides of the boundary. As g decreases with the capacity set held fixed, this lower bound increases stepwise. It does NOT prove that every pair of populations with ordered gaps has ordered stopping costs. The full vector determines the capacity set and the information in observations. The earlier homogeneous bound is the special case M=N, h=1-b in the increasing direction. This extension is an elementary corollary of the coupling argument, not a claimed new general lower-bound technique.

### A complementary sufficient condition for early certification

For uniform WoR sampling of d_i in [-1,1], fix alpha and set L=log(2N/alpha). A Hoeffding–Serfling interval at every t<N has radius

r_t=sqrt{2[1-(t-1)/N]L/t}

around the sample mean. Each interval has failure probability at most alpha/N; a union bound plus exact census yields simultaneous coverage at least 1-alpha. On that event its endpoints are within 2r_t of delta. For g>0, the interval therefore certifies the correct region whenever 2r_t<g. Define

t_0=min{N, floor[8L(N+1)/(Ng^2+8L)]+1}.

The corresponding decision procedure obeys P(tau<=t_0)>=1-alpha and E tau <=t_0+alpha(N-t_0). If t_0=N the statements follow from exact census. Otherwise they follow by solving 8[1-(t-1)/N]L/t<g^2 and applying the coverage event. This is a deliberately conservative existence bound built from an established concentration inequality, not a rate-optimal upper bound for direct betting.

Thus Ng^2 much larger than log(N/alpha) is a sufficient regime for a small high-probability evaluation fraction, while capacity-rich populations with Ng<h have an unavoidable large fraction. These scales leave a substantial gap. A variance-based finite-population approximation suggests a crossover in Ng^2/variance, but neither the lower nor upper result proves a universal sharp phase transition or a variance-sensitive minimax law. The distinction between a rigorous obstruction, a sufficient condition, and an empirical crossover is essential.

No optimality theorem for the proposed bet grid, no matching upper bound for every vector, no distribution-free savings for adaptive strata, and no population-generalization guarantee are claimed. Empirical absence of violations is not a proof. Comparisons of algorithms must separate formal validity, finite Monte Carlo error, and measured cost.

## 8. Direct directional betting and prediction-assisted signals

For a boundary mu_0 on the transformed [0,1] scale, let m_t(mu_0)=(N mu_0-S_{t-1})/R_t. On the null mu<=mu_0, factors 1+lambda(X_t-m_t(mu_0)) are nonnegative and have conditional expectation at most one when 0<=m_t(mu_0)<=1 and lambda belongs to the declared (0,1) grid. Use unit factors when that candidate conditional mean is outside [0,1]. If the bounded completion interval excludes the entire null, rejection is deterministically sound. The upper-direction factors use the minus sign and null mu>=mu_0. A fixed average of the eight products is a supermartingale under each respective null. Its first crossing of 2/alpha is a level-alpha/2 test.

Use four such tests: lower and upper directions at both -epsilon and +epsilon (transformed to [0,1]). A requires rejection of the lower-direction null at +epsilon; B requires rejection of the upper-direction null at -epsilon; E requires both inner-direction rejections. Conflicting evidence yields no certificate. If E is true, an error requires either of the two outer rejections. If A is true, an error requires an upper-direction rejection at +epsilon (for false E) or at -epsilon (for false B). If B is true the two lower-direction rejections play the corresponding role. In every case a union bound over two level-alpha/2 tests suffices. Strict tests may not certify a boundary before census; census returns the closed-region label exactly.

For the prediction-assisted adaptation, the charged pilot reveals a set O. Subsequent selection uses predictable q_i>0 on the remaining set J, with sum q_i=1, and predictable predictions p_i in [0,1]. Define the CELEUS finite-pool signal

Y = [sum_{i in O} x_i + sum_{i in J} p_i]/N + (x_I-p_I)/(N q_I).

Conditional on the past, E[Y]=mu, because the q-weighted correction averages to the remaining total residual divided by N. Put base=[sum_O x_i+sum_J p_i]/N. Valid predictable bounds are a=base-max_{i in J}p_i/(Nq_i) and b=base+max_{i in J}(1-p_i)/(Nq_i). Hence Z=(Y-a)/(b-a) is in [0,1] and has conditional expectation (mu-a)/(b-a). Apply the preceding directional factors to Z and candidate (mu_0-a)/(b-a). Unit factors handle candidates outside the signal support. The same two-event argument proves alpha correctness.

The estimator signal is adopted from CELEUS, not proposed as new. The implemented predictor is a nearest historical response profile selected using 64 charged pilot pair-items; reference selection and sampling weights are frozen thereafter. It is an explicitly documented adaptation, not a reproduction of the paper's surrogate-model experiments. Positive fixed weights generate a size-biased WoR permutation through independent exponential clocks; at each reveal the conditional selection probability is the item's weight divided by the remaining sum. Nonuniform selection is therefore accounted for exactly. No assumption that the predictor is accurate appears in the validity proof.

## 9. Joint stratified tests without alpha/H splitting

This is a specialization of established union-intersection stratified inference, not a claim to invent that approach. Let mu_h be the fixed transformed mean in stratum h, and w_h=N_h/N. For the first n_h observations of that stratum use the unweighted local statistics A_h=sum_j N_h/(N_h-j+1), Z_h=sum_j[X_{h,j}+S_{h,j-1}/(N_h-j+1)], and V_h=sum_j(X_{h,j}-p_{h,j})^2. Here p_{h,j} is a predictable local forecast in [0,1]. These remove the lambda and psi weights from the statistics in Section 3 because the weights are applied explicitly below. Set all three statistics to zero before the first observation. For a fixed lambda in (0,1) and direction s in {-1,+1}, the process

M_t(lambda,mu,s) = exp{ s lambda sum_h [Z_h-A_h mu_h] - psi(lambda) sum_h V_h }

is a nonnegative supermartingale at the true vector of stratum means under any predictable allocation that samples uniformly within the selected remaining stratum. To verify this, on a step in h write m for its true remaining mean. The increment of Z_h-A_h mu_h is X-m. The scalar inequality proved in Section 3 gives

E[exp{s lambda(X-m)-psi(lambda)(X-p)^2} | past]
<= exp{s lambda(p-m)}[1+s lambda(m-p)] <= 1.

Here |X-p|<=1, the scalar inequality applies to s(X-p), and 1+u<=exp(u) proves the second inequality with u=s lambda(m-p). All other strata's factors stay fixed. Predictability of the selected stratum establishes the claim in the global filtration. An average over the fixed lambda grid is also a supermartingale.

At each inspection let B_t be the Cartesian product of the deterministic completion intervals [S_h/N_h,(S_h+N_h-n_h)/N_h]. For the lower-direction composite null w dot mu<=m_0, minimize the mixture over B_t intersected with that null. If this set is empty, rejection is deterministically valid. Otherwise the minimizing vector maximizes A dot mu over that set: every lambda is positive, so the same vector minimizes every component of the mixture. Since A_h>=0, a maximizer can be taken on w dot mu=min(m_0,w dot hi). Starting at lo, fill coordinates in decreasing order of A_h/w_h until that weighted sum is attained. This fractional-knapsack solution is exact: transferring weighted mass from a smaller ratio to a larger unsaturated ratio cannot decrease the objective, which proves optimality by successive exchanges. The upper-direction null w dot mu>=m_0 instead minimizes A dot mu, fills in increasing ratio order, and uses boundary max(m_0,w dot lo).

Reject when this infimum reaches 2/alpha at any inspection. The infimum process itself need not be a supermartingale. Nevertheless, whenever the null is true its feasible set contains the true vector on every path. Crossing of the infimum therefore implies crossing of the true-vector mixture; Ville's inequality bounds its probability by alpha/2. The four directional tests at the two practical margins give alpha-correct ternary decisions by the same two-event argument as Section 8. Inspections every 16 observations restrict the rejection times and preserve validity; all observations between inspections are charged. Exact census supplies the terminal label. Adaptive allocation does not invalidate the argument, but no efficiency optimality follows.

Implementation checks compare 300 optimizations (150 random boxes, both directions) against an independent linear-programming solver and enumerate all 729 ordered ternary populations split into two strata, under each of two allocations. These checks supplement the proof; small-population tests alone cannot establish general error control.
