## Permutation Tests

Timothy Masters1
(1)
Ithaca, NY , **USA**
Overview of Permutation Testing
We begin with a general overview of the concept behind permutation testing. Of
necessity, many theoretical details are omitted; see my book Data Mining
Algorithms in C++ for more in-depth treatment. Suppose we are training or
testing some system and its performance depends on the order in which data is
presented to it. Here are some examples:
1. We have a completely defined trading system, and we want to measure its
performance out-of-sample. The order of price changes in its market price
history is of great consequence.
2. We have a proposed a market trading system, and we must optimize one or
more of its parameters to maximize a measure of its performance. The order
of price changes in its market price history is of great consequence.
3. We have a model that, on a regular basis, examines indicators and uses the
values of these variables to predict near-term changes in market volatility.
We want to train (optimize) this model, or test it on **OOS** data. We will then
measure the in-sample (if training) or out-of- sample (if testing) error of this
model. The order of the predicted variable, future volatility, with respect to
the order of the indicators is (of course!) of great consequence.
Although the precise details of how permutation testing would be employed
in each of these examples is somewhat different, the underlying idea is the same.
We perform whatever task we want (training or testing a trading system or
predictive model) using the original data in its correct order. Then we randomly
permute the data and repeat our training or testing activity, and we record the
result. Then we permute again, and again, many (hundreds or even thousands)
times. We compare the performance figure obtained from the original data with
the distribution of performance figures from the permutation results and thereby
may reach a conclusion.
How do we do this comparison? We are testing some measure of
performance, whether it be the net return of a trading system, the mean error of a
predictive model, or any other performance measure appropriate to our
operation. Our operation may or may not be useful: our trading system may or
may not be able to legitimately capitalize on market patterns to make money.
Our predictive model and the indicators on which it bases its decisions may or
may not have true predictive power. But there’s one thing we can usually be
quite sure of: if we permute the data on which our operation is based, any
legitimate ability will vanish because predictive patterns are destroyed. If we
randomly permute the price changes in a market history, the market will become
unpredictable, and hence any trading system will be hobbled. If we randomly
change the pairing between indicators and a target variable for a predictive
model, the model will not have any authentic relationships to learn or make use
of.
This leads to our method for using permutation testing. Suppose for the
moment that we repeat the training or testing with nine different permutations.
Including the original, unpermuted data, we have ten performance measures. If
we sort these, the original performance can occupy any of the ten possible
ordered positions, from best to worst, or any position in between. If our
operation is truly worthless (the trading system has no ability to detect profitable
market patterns or the model has no predictive power), then the original order
will have no advantage. Thus, the original performance has an equal probability
of occupying any of the positions. Conversely, if our operation has legitimate
power, we would expect that its original performance would come in at or near
the best. So, the position of our original performance in the sorted performances
provides useful information about the ability of our operation.
We can be more rigorous. Continue to suppose that we have performed nine
permutations. Also suppose we find, to our great joy, that the original
unpermuted data has the best performance of the ten values. This, of course, is
great news and very encouraging. It is evidence that our operation is finding
useful patterns in the data when the data is not permuted. But how meaningful is
this finding? What we can say is that if our operation is truly worthless there
would be a 0.1 probability that we would have obtained this result by sheer luck.
In other words, we have obtained a p-value of 0.1. If this conclusion and
terminology are not perfectly clear, please review the material on hypothesis
tests that begins on page **210**.
What if our original performance is the second best of the ten performers?
Under the null hypothesis that our operation is worthless, there is a 0.1
probability of it landing in that second slot, and also a 0.1 probability that it
would have done better, landing in the top slot. Thus, there is probability (p-
value) of 0.2 that a worthless operation would have obtained the performance we
observed, or better.
In general, suppose we perform m random permutations, and also suppose
that the performance of k of these permutations equals or exceeds the
performance of the original data. Then, under the null hypothesis that our
operation is worthless, there is probability (k+1)/(m+1) that we would have
obtained this result or better by luck.
If we want to be scrupulously rigorous in our experimental design, we would
choose a p-value in advance of doing the permutation test. In particular, we
would choose a small probability (typically 0.01 to 0.1) that we find to be an
acceptable likelihood of falsely concluding that our operation has legitimate
ability when it does not. We would choose a large m (over 1,**000** is not unusual
or excessive) such that m+1 times our p-value is an integer, and solve for k. Then
perform the permutation test and conclude that our operation is worthy if and
only if k or fewer of the permuted values equal or exceed the original value. If
our operation is truly worthless, there is our chosen probability that we will
falsely conclude that it is worthy.
Testing a Fully Specified Trading System
Suppose we have developed a trading system and we want to test its
performance on a set of market history that we held out from the development
process. This will give us an unbiased performance figure. We have already
explored some important uses for returns obtained in this out-of-sample time
period. If none of the returns is extreme and the shape of their distribution is
roughly bell-curve-shaped, we can cross our fingers and use the parametric tests
described on page **216**. If we want to be more conservative, we can use the
bootstrap test described on page **222**. But as we’ll see soon, a permutation test
provides a potentially valuable piece of information not provided by either of the
tests just mentioned.
Moreover, permutation tests have none of the distribution assumptions that
limit utility of parametric tests, and they are even more robust against
distribution problems than bootstrap tests. Thus, permutation tests are a vital
component of a well-equipped toolbox.
When we permute market price changes to perform this test, we must
permute only the changes in the **OOS** time period. It is tempting to start the
permutation earlier, with the price changes that drive the trade decisions. For
example, suppose we look back **100** bars to make a trade decision. The data for
our test will start **100** bars before the beginning of the **OOS** test period so that we
can begin making trade decisions immediately, on the first bar of the **OOS**
period. But these **100** early bars must not be included in the permutation. Why?
Because their returns will not be included in the original, unpermuted
performance figure. What if these early bars are unusual in some way, such as
having a strong trend? When these unusual bars get permuted into the **OOS**
segment, they would impact results relative to the original result which does not
include their influence. So, they must not be allowed to invade the **OOS** test
area.
Testing the Training Process
Perhaps the single most important use of permutation testing is evaluation of the
process by which your trading system is optimized. There are primarily two very
different ways in which a trading system can fail. The most obvious failure mode
is that the system is not able to detect and capitalize on predictive patterns in
market prices; it’s weak or unintelligent. It should be apparent that permutation
testing will easily detect this situation, because the performance of your system
on unpermuted data, as well as on permuted data, will be poor. Y our system’s
performance will not stand out above the permuted competition.
However, this is not the situation we are most interested in, because we
would almost certainly never get this far. The weakness of a trading system will
be apparent long before we reach the point of expending precious computer
resources; we’ll see the dismal performance quickly.
The problem in which permutation testing is valuable is the opposite of
weakness: your system is too powerful at detecting predictive patterns. The term
commonly employed for this situation is overfitting . When your system has too
many optimizable parameters, it will tend to see random noise as predictive
patterns and learn these patterns along with any legitimate patterns that might be
present. But because noise does not repeat (by definition), these learned patterns
will be useless, even destructive, when the system is put to use trading real
money. I have often seen people develop systems that look back optimizable
distances for several moving averages, optimizable distances for volatility, and
optimizable thresholds for changes in the quantities. Such systems produce
astonishing performance in the training period and yet produce completely
random trades out-of-sample.
This is where permutation testing comes to the rescue. An overfitted trading
system will perform well not only on the original data but on permuted data as
well. This is because an overfitted system is so powerful that it can learn
“predictive” patterns even on permuted data. As a result, all in-sample
performances, permuted and unpermuted, will be excellent, and the original
performance will not stand out from its permuted competitors. So, all you need
to do is repeat the training process on many sets (at least **100**) of permuted data
and compute the p-value as described earlier, (k+1)/(m+1). This may require a
lot of computer time, but it is almost always worthwhile. In my own personal
experience working with trading system developers over the years, I have found
this technique to be one of the most valuable tools in my toolbox. Unless you get
a small (0.05 or less) p-value, you should be suspicious of your system
specification and optimization process.
Walkforward Testing a Trading System Factory
In many or most development situations, we have an idea for a trading system,
but our idea is not fully specified; there are one or more aspects of it, such as
optimizable parameters, that are left unspecified. As a simplistic example, we
may have a moving-average crossover system that has two optimizable
parameters, the long-term and short-term lookbacks. The system definition,
along with a rigorously defined method for optimizing its parameters, and
verified by **OOS** testing of the system, make up what we might call a model
factory . In other words, prior to optimization we do not have an actual trading
model; it’s just an idea along with a way of converting the idea into something
concrete. The actual trading system we end up with will depend on the market
data on which it is trained. Our goal now is to assess the quality of our model
factory, as opposed to assessing the quality of a completely defined trading
system. If we are able to conclude that our model factory is probably effective at
producing good trading systems, then when we use up-to-date data to create a
trading system from the model factory, we can be confident that our system will
have respectable performance. This, of course, is the whole idea behind
walkforward testing that we have explored from numerous different angles in
prior chapters. But the distinction between testing complete systems versus
testing our training process versus testing our model factory is especially
pertinent to permutation testing. This is the reason for emphasizing this
distinction here.
When we mate permutation testing with walkforward testing, we have to be
careful about what is permuted, just as we did when testing a fully specified
system. In particular, consider the fact that when we walk the original
unpermuted system forward, the training data in the first fold will never appear
in any **OOS** area. Since this section of historical data may contain unusual prices
changes such as large trends, we must make sure it never appears in the **OOS**
area of permuted runs. Thus, the first training fold must be omitted from
permutation.
Do we also permute the first training fold that is omitted from the **OOS**
permutation? I’ve never seen any convincing argument for or against this, and
my gut instinct is that it makes little difference. However, my own practice is to
also permute the first training fold, in isolation, of course. This would likely
provide more variety in trade decisions. For example, it may be that the original
data leads to a large preponderance of, say, long positions in the first **OOS** fold.
If the market overall has a strong upward bias, this would inflate permuted
performance. But if permuting the first training fold often reduces the number of
long positions, this would give more variety of trade outcomes, which is our
ultimate goal in a permutation test. On the other hand, I do not consider this to
be an overwhelming argument, so if you chose to avoid permuting the first
training fold, I don’t think you will be committing a grave sin.
Another decision concerns if and how to permute walkforward folds. There
are two choices. Y ou can do a single permutation of all market changes after the
first training fold and then just do the walkforward on this permuted data.
Alternatively, you can do a separate, isolated permutation with each fold. Y ou
could even break this second alternative into several subalternatives, pooling the
IS and **OOS** data in each fold into a single permutation group or separating the
IS and **OOS** sets of each fold into separately permuted groups.
What is the difference between these alternatives? Honestly, not enough
research has been done to provide rigorous guidance in this choice. It seems that
the dominant factor involves stationarity in market behavior. If you want to
assume that the characteristics (especially trend and volatility) of the market are
constantly changing and you want your testing method to adapt to these ever-
changing conditions, then you would likely want to permute each fold separately
to preserve local behavior. Personally, I prefer to focus on market patterns that
are universal, as opposed to trying to track perceived changes and be vulnerable
to whipsaws. For this reason, my own habit is to permute all market changes
after the first fold’s training set as a single large group. But I claim no special
knowledge or expertise in this matter. All I can say is that this is what makes the
most sense to me, and it is what I do in my own work. Feel free to disagree.
Regardless of how you choose to permute, you will have an **OOS**
performance figure for the original, unpermuted data, as well as a similar figure
for each permutation. As in the other tests, all you have to do is count how many
of those permuted performances equal or exceed that of the original data. Use
the p-value = (k+1)/(m+1) formula, which gives the probability that your original
**OOS** performance could have been as good as or better than what you obtained
by sheer luck from a truly worthless model factory. Unless this p-value is small
(0.05, or even 0.01 or less) you should doubt the quality of your factory and
hence mistrust any trading system produced by it.
Permutation Testing of Predictive Models
Everything so far has concerned trading systems. But financial market traders
may use predictive models to do things such as predict upcoming changes in
volatility. It is often the case that variables other than market price histories are
involved, things such as economic indicators or concurrent forecasts of other
quantities. These are typically called predictors because they are the quantities
used by the model to make predictions. We also have a “truth” variable, usually
called the target variable . This is the quantity that we are trying to predict, and
to train the predictive model we need to know the true value of the target that
corresponds to each set of predictors. In the volatility example, the target would
be the near-term future change in volatility.
In discussing trading systems, we identified three situations: 1) testing a fully
specified system on out-of-sample data; 2) testing our training process, with a
special eye on detecting overfitting; and 3) testing our model factory.
Permutation testing of predictive models falls into the same three categories in
what should be an obvious manner, so we will not distinguish between them in
this discussion. Rather, we will focus on special aspects of permutation.
Understand that in the context of pairing targets with predictor sets, for the
vast majority of models the order in which training data appears is irrelevant. It
is only the pairing of predictor sets with targets that impacts training. We want
them to be concurrent: we pair the correct value of the target at a given time with
the current values of the predictors. We permute by disrupting this pairing,
randomly reordering the targets so that they become paired with different
predictor sets. When we do this, there are two vital issues, both of which will be
described in more detail soon.
1. Indicator sets must not permute with respect to one another, only with
respect to the target. This preserves intraset correlation, which is critical to
correct testing.
2. There must not be any serial correlation in both one or more predictors and
the target. Serial correlation in one or the other is fine, even common, but it
must not be present in both.
For the first issue, consider this toy example. Suppose we have two
predictors: recent trend of the S&P **100** index and recent trend of the S&P **500**
index. These two quantities are used to predict the volatility of S&P **100** next
week relative to its volatility in the week just ended. At the close of trading
every Friday we compute these two recent trends as well as the volatility during
the week that just ended. When we train our predictive model on historical data,
we also know the volatility during the upcoming week, so we subtract the prior
week’s volatility from the upcoming week’s volatility to get the change, which is
our target variable. When we put the trained model to use, we will predict the
upcoming change in volatility.
The correct way to permute this data is to randomly reorder the targets so
that targets get attached to pairs of predictors that are from different weeks, thus
destroying any relationship that could be predictive. What if we also permuted
the predictors? If we did that, we would often get nonsensical predictor pairs. We
might end up with a predictor pair in which S&P **100** has a strong uptrend while
S&P **500** has a strong downtrend. In real life, this sort of pairing would be
extremely unlikely, if not impossible. One key idea behind permutation testing is
that we must create permutations that could have occurred in real life with equal
probability under the null hypothesis that the model is worthless. If we generate
nonsensical or highly unlikely permutations, the method fails.
For the second issue, consider that one or more of the predictors may have
serial correlation (the value of a variable at a given time is related to its value at
nearby times). In fact, this is extremely common, almost universal. For example,
suppose a predictor is the trend over the prior 20 bars. When we advance by one
bar, we still have 19 of the prior 20 bars going into the calculation, so the trend is
unlikely to change much.
If we are not careful, the target variable may have serial correlation as well.
For example, in the volatility example I defined the target as the change in
volatility, not the actual volatility. If we use volatility as the target, we will find
significant serial correlation, because volatility usually changes slowly; the
volatility next week will be close to the volatility this week. But changes in
volatility are much less likely to have serial correlation. Of course, it may still
exist, but certainly it will be greatly reduced, if not totally eliminated.
Even change in volatility will have serious serial correlation if we have
overlapping time periods. For example, suppose that on each day of the week,
five days a week, we compute the change in volatility over the upcoming five
days and compare it to the prior five days. Each time we advance the window,
most days will be in common, so successive values of volatility change will be
highly correlated.
The key point is that serial correlation in just one or more predictor variables,
or in just the target, is harmless. This is because we can then view permutation as
permuting whichever is not serially correlated and avoid destroying the serial
correlation in the other. But if both are serially correlated, permutation will
destroy this property, and we will be in the situation of processing pairings that
could not occur in real life, a major sin. Recall once more that a key tenet of
permutation testing is that our permutations must have equal probability in real
life if our model is worthless.
It’s worth noting that this serial correlation restriction is not unique to
permutation tests. This restriction is shared by virtually all standard statistical
tests. The fact that some observations are dependent on other observations
effectively reduces the degrees of freedom in the data, making tests behave as if
there are fewer observations than there really are. This leads to an increased
probability of rejecting the null hypothesis, the worst sort of error.
### The Permutation Testing Algorithm
Most readers should be fairly clear by now on how a permutation test, often
called a Monte Carlo permutation test (**MCPT**) , is performed. However, we will
now ensure the clarity of the informal presentation by stating the algorithm
explicitly. In the following pseudocode, nreps is the total number of
evaluations, including the original, unpermuted trial. Each trial results in a
performance figure being found, with larger values implying better
performance. If we are testing a fully specified trading system or predictive
model, this is the performance obtained on an out-of-sample set. If we are testing
our training process, this is the final (optimal) in-sample performance. If we are
testing a model factory, this is the performance obtained by pooling all **OOS**
folds. To be compatible with C++, zero origin is used for all array addressing.
for irep from 0 through nreps-1
if (irep > 0)
shuffle
compute performance
if (irep == 0)
original
_performance = performance
count = 1
else
if (performance >= original
_performance)
count = count + 1
p-value = count / nreps
We compute the performance on the unshuffled data first and save this
performance in original
_performance. We also initialize our counter of
the number of times a computed performance equals or exceeds the original
performance. From then on we shuffle and evaluate the performance on shuffled
data, incrementing the counter as indicated. The p-value is computed using the
formula already seen several times, (k+1)/(m+1), where k is the number of times
a permuted value equals or exceeds the original value, and m is the number of
permutations. We’ll explore several programs demonstrating this algorithm at
the end of this chapter.
Extending the Algorithm for Selection Bias
On page **124** we began an extended discussion of selection bias. If necessary,
please review all of that material. Here we show how Monte Carlo permutation
testing) can be extended to handle selection bias. To put this topic in context,
here is a common scenario. We have several competing trading systems, say two
or maybe hundreds. Perhaps they have been submitted by different developers
for our consideration, or perhaps they are all the same basic model but with
different trial parameter sets. In any event, we choose the best from among the
competitors. There are two questions that this algorithm will answer.
1. The less important but still interesting question concerns the competitors
taken individually. For each competitor (ignoring other competitors), what
is the probability that we would have obtained performance as least as good
as what we observed if that competitor were actually worthless? This is
exactly the same question answered by the basic algorithm shown in the
prior section, answered separately for each competitor.
2. The really important question concerns the best (highest performing)
competitor. Suppose all of the competitors are worthless. If we test a large
number of them, it is likely that at least one will be lucky and do well by
sheer random chance. Thus, we cannot just determine which one is the best
performer and then use what might be called its solo p-value, the probability
that if it were worthless it would have done as well as it did by sheer luck.
This is the p-value computed by the algorithm in the prior section. Such a
test would be strongly prejudiced by the fact that we picked the best system.
Of course, it’s going to do well on a solo test! So, we have to answer a
different question: if all the competitors are worthless, what is the
probability that the best of them would have performed at least as well as
what we observed? We might call this the unbiased p-value because it takes
into account the bias induced by selecting the best competitor.
The algorithm for answering these two questions is shown here.
for irep from 0 through nreps-1
if (irep > 0)
shuffle
for each competitor
compute performance of this competitor
if (irep == 0)
original
_performance[competitor]
= performance
solo
_
count[competitor] = 1 ;
unbiased
_
count[competitor] = 1 ;
else
if (performance >=
original
_performance[competitor])
solo
_
count[competitor] =
solo
_
count[competitor] + 1
if (irep > 0)
best
_performance = **MAX** ( performance of
all competitors )
for each competitor
if (best
_performance >=
original
_performance[competitor)
unbiased
_
count[competitor]
= unbiased
_
count[competitor] + 1
for all competitors
solo
_pval[competitor] =
solo
_
count[competitor] / nreps
unbiased
_pval[competitor] =
unbiased
_
count[competitor] / nreps
Readers should examine this algorithm and confirm that for each individual
competitor, the solo
_pval computed here is exactly the same as would be
computed by the algorithm in the prior section for any individual competitor.
Note that this algorithm computes an unbiased
_pval for every
competitor. For each permutation, it finds the best performer and compares this
to the score for each competitor, incrementing the corresponding counter
accordingly. For whichever competitor had the best original performance, this is
a perfect apples-to-apples comparison, best-to-best, and hence this is a correct p-
value for the best performer. For all other competitors, this p-value is
conservative; it is an upper bound for the true p-value. Thus, any competitor that
has a small unbiased
_pval is worthy of serious consideration.
Partitioning Total Return of a Trading System
Suppose you have just trained a market trading system, optimizing its parameters
in such a way as to maximize a measure of performance. On page **286** we saw
how a Monte Carlo permutation test could be used to gather information about
whether the model is too weak (unable to find predictive patterns) or too strong
(overfitting by mistaking noise for authentic patterns). We also saw ways to
employ permutation testing to evaluate a completely specified model using **OOS**
data and also a way to evaluate the quality of a trading-system factory. Now we
look at one more interesting way to use permutation testing to gather information
about the quality of a trading system. This method is not quite as rigorous as the
prior tests, and its results should usually be taken with a liberal grain of salt. But
its development reveals much about how seemingly good performance is
obtained from a trading system, and the technique also provides one more
indication of possible future performance.
Suppose we have just trained a trading system by adjusting its parameters so
as to maximize a performance measure. We can roughly divide its total in-
sample return into three components.
1. Our model (hopefully!) has learned legitimate Skill at detecting predictive
patterns in the market history and thereby making intelligent trade
decisions. This component of performance will likely continue into the
future.
2. Our model has also mistaken some noise patterns as legitimate and thereby
learned responses to patterns that, by definition, will not repeat. This
component of performance, called TrainingBias , will not continue into the
future.
3. If the market has an overall long-term trend (like most equity markets,
which trend upward over the long term), most training algorithms will favor
a position that takes advantage of the trend. In particular, it will favor long
positions for up-trending markets and short positions for down-trending.
This Trend component of performance will continue into the future for only
as long as the trend continues.
This last component deserves more discussion, especially since it is the
subject of controversy among some trading system developers. Imagine that you
have trained a trading system (optimized its parameters) on two equity markets,
individually. Market A has a strong uptrend over its training-set history, while
market B ends its history at about the same price level as where it began. Y ou
find that the optimal parameters of your Market A trading system provide a great
preponderance of long trades, while the optimal parameters for the system
trained on Market B give about an equal number of long and short trades. It
doesn’t take Sherlock Holmes to deduce that the reason for the abundance of
long trades in the system developed on Market A might have something to do
with the fact that Market A enjoyed steady gains, while the long/short balance in
the other system is due to the fact that Market B had no appreciable trend.
The big philosophical question is this: should we let the underlying long-
term trend of a market exert that much influence on the long/short trade balance
of a system we are designing? In my own experience, I have found that most
trading system developers do so without even thinking about the issue. And I
tend to agree with this philosophy; if a market has an obvious long-term trend,
we might as well go with the flow instead of fighting a current by rowing
upstream.
On the other hand, it is definitely worthwhile pondering the alternative. After
all, who’s to say that a long-term trend will continue, and what happens to a
strongly unbalanced system if the trend reverses? This is one argument against
letting a strongly trending market strongly influence our trade balance.
There’s an even deeper way of looking at the issue. Suppose, for example,
that we have a strongly uptrending market and that we have developed a long-
only day-bar system that is in this market half of all trading days. Consider the
fact that if we just flip a coin every day and take a long position when it comes
up heads, we would also, on average, make a lot of money just from the trend.
So one could easily argue that a trading system’s “intelligence” should be
measured by the degree to which it beats a hypothetical random trading system
that has the same number of long and short positions.
It all boils down to a simple but fraught question. If your system makes a lot
of money from a trend but can’t beat a coin toss, is it really any good? One
school of thought says that if it ties a profitable coin-toss system, it has no
intelligence. Another school of thought says that the very fact that it was able to
capitalize on a long-term trend is a sign of intelligence. Then the sage in the
corner points out that the second argument falls apart if the trend reverses, while
the first argument is more likely to hold up. Y et another voice pipes up from the
shadows, pointing out that long-term trends generally persist over the, well, long
term. And the argument goes on.
Regardless of your opinion, it’s worthwhile to explore this issue further. As
usual throughout this book, we regard returns as the log of changes. Let
MarketChange be the total change over the extent of the market history in our
training set. Under our definition of change, this is the log of the ratio of the final
price to the first price. Let n be the number of individual price change returns
(one less than the number of prices). Then we can define TrendPerReturn =
MarketChange / n.
Some developers subtract this quantity from the return of every bar during
optimization to remove the effect of trend on computed performance. (Of course,
when computing indicators or anything else involved in making trade decisions,
one would use the original prices. This correction is used only for computing
performance measures such as return, profit factor, or Sharpe ratio.) This option
can be applied to any of the trading systems used as examples in this book, and
indeed virtually every trading system anyone could imagine. However, other
than this brief mention, we will not pursue this idea further. At this time, we
have a different use for trend.
What would be the expected total return of a random trading system having
the same number of long and short positions as our trained system? For every
individual price-change return during which we hold a long position, on average
the trend will boost our return by TrendPerReturn . Conversely, for every one in
which we hold a short position, our return will be decreased by TrendPerReturn.
So, the net effect will be the difference in these position quantities.
In keeping with the nomenclature presented in the beginning of this section,
we define the Trend component of the system’s total return as shown in Equation
7-1.
(7-
1. Because we can compute TrendPerReturn from the market price history and
because we know the position counts from the trained system, the Trend
component of the system’s total return can be explicitly computed.
Recall that the underlying premise for the material in this section is that the
total return of our trained trading system is the sum of three components:
legitimate skill, long/short imbalance that capitalizes on trend, and training bias
(learning random noise as if it were real patterns). This is expressed in Equation
7-2.
(7-
2. Suppose we were to randomly permute the market changes and retrain the
system. The TrendPerReturn will remain the same because we’re just mixing up
the order of price changes, and we still have the same number of individual
returns. But the number of long and short positions will likely change, so we
have to use Equation 7-1 to compute the Trend component of the total return for
this permuted run. Because the permutation is random, we have destroyed
predictable patterns, so the Skill component is zero. Any total return over and
above the Trend component is TrainingBias . In other words, we can compute
the TrainingBias for this permuted run using Equation 7-3.
(7-
3. Too much randomness is involved for a single such test to provide a useful
estimate of the TrainingBias inherent in your proposed trading system and its
training algorithm. But if we perform hundreds, or even thousands, of
permutations and average the value computed by Equation 7-3, we can arrive at
a generally respectable estimate for TrainingBias.
This lets us compute two extremely useful performance figures. First, we can
compute an unbiased estimate of future return by subtracting the training bias
from the total return of our system. This figure includes the Trend component of
total return, appropriate if we hold to the philosophy that taking advantage of
long-term trend is good. This is expressed in Equation 7-4.
(7-
4. If we are also interested in the more restrictive definition of trading system
intelligence, the degree to which our system can outperform a random system
having the same number of long and short trades, we can estimate its Skill using
Equation 7-5.
(7-
5. We will explore a program that demonstrates this technique on page **310**.
Essential Permutation Algorithms and Code
Before presenting complete programs that demonstrate the techniques discussed
in this chapter, we’ll focus on several of the key permutation algorithms that will
be essential tools for this family of tests.
### Simple Permutation
We begin with the basic permutation algorithm. This is the standard method for
correctly permuting a vector, doing it in such a way that every possible
permutation is equally likely. It requires a source of uniformly distributed
random number in the range 0.0 <= unifrand() < 1.0. It is important to make
sure that the random generator can never return exactly 1.0; if you cannot be
sure of this, you must take appropriate action to ensure that an out-of-bound
subscript is not generated. In the following code, the random j must be strictly
less than i.
i = n ; shuffled
while (i > 1) { shuffle
j = (int) (unifrand () * i) ;
--i ;
itemp = indices[i] ; i and j
indices[i] = indices[j] ;
indices[j] = itemp ;
}
// Number remaining to be
// While at least 2 left to
// Swap elements
In this code, we initialize i to be the number of elements in the vector, and at
each pass through the while() test, it will be the number remaining to be
shuffled. We randomly select an index j that is equally likely to point to any of
the elements yet to be shuffled. Decrement i so that it points to the last element
in the aray that remains to be shuffled and swap elements j and i. Note that it is
possible that j==i so that no swap takes place. We work backwards from the
end of the array to the front, stopping only when we no longer have anything to
swap.
### Permuting Simple Market Prices
We jump to a slightly higher level of difficulty when we permute market prices.
Obviously we can’t just swap prices around. Imagine what would happen if we
permuted decades of equity prices whose market history begins at 20 and ends at
## So we have to deconstruct the price history into changes, permute the
changes, and then reconstruct the permuted price history. Moreover, we can’t
permute simple differences in price, because differences at large price times are
greater than differences at small price times. So, we compute the changes as
ratios. Equivalently, we take the log of prices and permute the changes in logs.
Another complication is that we must exactly preserve the trend in the price
history so that position imbalances are handled correctly. This is easy to do; we
just keep the starting price the same. Since the reconstructed price series applies
the same changes, just in a different order, we end up at the same price in the
end. Only the ups and downs in the interior are changed.
The first step is to deconstruct the price history into changes. The following
simple code assumes that the supplied prices are actually the log of the original
prices. We must supply the work area changes, which is nc long. Note that the
last element of changes is unused.
void prepare
_permute (
int nc , // Number of
cases
double *data , // Input of nc log
prices
double *changes computed changes
// Work area; returns
)
{
int icase ;
for (icase=1 ; icase<nc ; icase++)
changes[icase-1] = data[icase] - data[icase-
1] ;
}
That preparation code needs to be done only once. From then on, any time
we want to permute the (log) price history, we call the following routine:
void do
_permute (
int nc , // Number of
cases
double *data , shuffled prices
double *changes changes from prepare
_permute
)
// Returns nc
// Work area; computed
{
int i, j, icase ;
double dtemp ;
// Shuffle the changes. We do not include the
first case in the shuffling,
// as it is the starting price, so there are
only nc-1 changes.
i = nc-1 ; remaining to be shuffled
while (i > 1) { least 2 left to shuffle
j = (int) (unifrand() * i) ;
if (j >= i) not happen, be safe
j = i - 1 ;
--i ;
dtemp = changes[i] ;
changes[i] = changes[j] ;
changes[j] = dtemp ;
} // Shuffle the changes
// Number
// While at
// Must
// Now rebuild the prices, using the shuffled
changes
for (icase=1 ; icase<nc ; icase++)
data[icase] = data[icase-1] + changes[icase-
1] ;
}
Recall that prepare
_permute() left the last element in changes
unused, so we have nc–1 changes to shuffle. We assume that the caller has not
changed the first element in data, and we rebuild from there.
Permuting Multiple Markets with an Offset
As was pointed out earlier, if our trading system references multiple markets, we
must permute them all the same way so that inter-market correlation is kept
intact. Otherwise, we might end up with market changes that would be
nonsensical in the real world, with some markets going up strongly while other
markets with which they are highly correlated going down strongly. This lack of
real-world conformity would be devastating, because a key tenet of Monte Carlo
permutation testing is that all permutations must be equally likely if the null
hypothesis is true.
To be able to do this, we must make sure that every market has a price on
every date; any dates for which one or more markets have no price must be
removed. In practice, if we stick with broadly traded markets, we generally lose
few or no dates because they all trade on normal trading days. If markets are
closed for a holiday, nothing trades, and if they are open for normal business,
everything trades. Still, we must make sure that there is no missing data for any
date, which would make simultaneous permutation impossible. A fast algorithm
for doing this is as follows:
Initialize each market's current index to 0
Initialize the grand (compressed) index to 0
Loop
Find the latest (largest) date at each
market's current index across all markets
Advance all markets' current index until the
date reaches or passes this date
If all markets have the same current date:
Keep this date by copying market
records to the grand index spot
Advance each market's current index as
well as the grand index
In the code that follows, we have the following:
market
_
n[]: For each market, the number of prices present
market
_price[][]: For each market (first index) the prices (second
index)
market
_
date[][]: For each market (first index) the date of each price
(second index)
market
_
index[]: For each market, the index of the record currently being
examined
grand
_
index: The index of the current record in the compressed data
for (i=0 ; i<n
_
markets ; i++) // Source
markets all start at the first price
market
_
index[i] = 0 ;
grand
_
index = 0 ; //
Compressed data starts at first record
for (;;) {
// Find max date at current index of each market
max
_
date = 0 ;
for (i=0 ; i<n
_
markets ; i++) {
date = market
_
date[i][market
_
if (date > max
_
date)
max
_
date = date ;
index[i]] ;
}
// Advance all markets until they reach or pass
max date
// Keep track of whether they all equal max
_
date
all
same
date = 1
_
_
; // Flags if all
markets are at the same date
for (i=0 ; i<n
_
markets ; i++) {
while (market
_
index[i] < market
_
Must not over-run a market!
date = market
_
if (date >= max
date[i][market
date)
_
_
n[i]) { //
index[i]] ;
break ;
++market
_
index[i] ;
}
if (date !=
max
_
date) // Did some
market jump over max?
all
same
_
_
date = 0 ;
market
_
if (market
n[i]) _
index[i] >=
// If even one market runs out
break
; //
We are done
}
if (i <
n
_
markets) //
If even one market runs out
break
; //
We are done
// If we have a complete set for this date, grab
it
if (all
same
_
_
date) {
for (i=0 ; i<n
_
markets ; i++) {
market
_
date[i][grand
_
index] = max
_
; // Redundant, but clear
market
_price[i][grand
_
index] =
market
_price[i][market
_
index[i]] ;
++market
_
index[i] ;
}
++grand
_
index ;
date
}
n
}
_
cases = grand
_
index ;
We are now ready to consider the permutation of multiple markets. It will
often be the case that we want to permute different sections of the market history
separately. If we are permuting a single market, this is easily done by just
offsetting the price in the calling parameter for the permutation routine. But
when we have an entire array of markets, we can’t do this, so we have to
explicitly specify an offset distance.
Here is how the permutation will be done. We have nc cases from price
index 0 through nc–1. Case offset is the first case that will change, and
offset must be positive because the case at offset–1 is the “basis” case and
remains unchanged. The last case examined is at nc–1, but it, too, will remain
unchanged. Thus, the shuffled array starts and ends at the original prices. Only
the interior prices change.
If a dataset is permuted in separate sections, the sections must not overlap.
The “basis” case at offset–1 is included in the region that cannot overlap. For
example, we could permute with offset=1 and nc=5. Cases 1 through 3
would then change, with the end cases (0 and 4) remaining unchanged. A
subsequent permute must then begin at offset=5 or more. Case 4 is not
changed by either permute operation.
Here is the preparation routine that must be called first and only once if
multiple permutations are done:
void prepare
_permute (
int nc , cases total (not just starting at offset)
int nmkt , // Number of
// Number of
markets
int offset , case to be permuted (>0)
double **data , price matrix
double **changes computed changes
)
// Index of first
// Input of nmkt by nc
// Work area; returns
{
int icase, imarket ;
for (imarket=0 ; imarket<nmkt ; imarket++) {
for (icase=offset ; icase<nc ; icase++)
changes[imarket][icase] = data[imarket]
[icase] - data[imarket][icase-1] ;
}
}
The permutation is just a simple generalization of the single-market method
shown in the prior section.
void do
_permute (
int nc , cases total (not just starting at offset)
int nmkt , // Number of
// Number of
markets
int offset , // Index of first
case to be permuted (>0)\
double **data , // Returns nmkt by nc
shuffled price matrix
double **changes // Work area; computed
changes from prepare
_permute
)
{
int i, j, icase, imarket ;
double dtemp ;
// Shuffle the changes, permuting each market
the same to preserve correlations
i = nc-offset ; to be shuffled
while (i > 1) { left to shuffle
j = (int) (unifrand() * i) ;
if (j >= i) happen, but be safe
j = i - 1 ;
--i ;
// Number remaining
// While at least 2
// Should not
for (imarket=0 ; imarket<nmkt ; imarket++) {
dtemp = changes[imarket][i+offset] ;
changes[imarket][i+offset] =
changes[imarket][j+offset] ;
changes[imarket][j+offset] = dtemp ;
}
} // Shuffle the changes
// Now rebuild the prices, using the shuffled
changes
for (imarket=0 ; imarket<nmkt ; imarket++) {
for (icase=offset ; icase<nc ; icase++)
data[imarket][icase] = data[imarket]
[icase-1] + changes[imarket][icase] ;
}
}
### Permuting Price Bars
Permuting price bars is considerably more involved than permuting a simple
array of prices. There are four major issues to consider, and perhaps a few other
more minor issues that may be relevant in some circumstances. These are
important:
We must never let the open or close be outside the range defined by the high
and low of the bar. Even if our trading system ignores the high and low,
violating this basic tent is bad karma.
If our trading system examines the high and low of bars, we must not damage
the statistical distribution of these quantities, either in regard to their
relationship to the open and close or in regard to their spread. These quantities
must have the same statistical properties after permutation as before.
We must not damage the statistical distribution of the price change as we
move from the open of the bar to the close. The distribution of open-to-close
changes must be the same after permutation as before permutation.
We must not damage the statistical distribution of the inter-bar gaps, the price
change between the close of one bar and the open of the next bar. This is
much more important than you might realize and easy to get wrong if you are
not careful.
Satisfying the first three conditions is easy. We just define the high, low, and
close in terms of the open. If we are (as usual) dealing with the log of prices, for
each bar we compute and save the high minus the open, the low minus the open,
and the close minus the open. Then, when we have a new opening price, we add
these differentials to it to get the new high, low, and close, respectively. As long
as we keep these trios of differences together (do not swap a high difference in
one bar with a low difference in another bar), it should be obvious that the first
condition is satisfied. And as long as our permutation algorithm does not alter
the statistical distribution of the open, it should be clear that the second and third
conditions are satisfied. The fourth condition is the monkey wrench.
The intuitive way to permute bars is severely incorrect. Suppose we just
permute the opens in the same way that we have been permuting single price
arrays: compute the open-to-open changes, permute these changes, rebuild the
array of opens, and use the “three differences” method just discussed to complete
each bar. As already pointed out, the first three conditions are satisfied by this
algorithm.
But here’s the problem. Remember that most of the time, a bar opens very
close to where the prior bar closed, often at exactly the same price. However,
under this incorrect permutation algorithm, it will often happen that we will have
an unfortunate combination of two common events: we have a large increase in
the permuted open-to-open change, and the first bar has a large open-to-close
drop in price. The result is a gigantic, completely unrealistic gap in the close-to-
open change.
For example, we might have a bar that opens at **100** and closes at 98, not
unrealistic. The next bar should open very near 98. But at the same time, the next
permuted open might be **102**, also not unrealistic. The result is a move from 98
to **102** just going from the close of one bar to the open of the next bar. The
chance of this happening in real life is nearly zero. And of course, the opposite
could happen as well: we have a bar with large upward movement open-to-close,
while the permuted open-to-open move to the next bar is a large drop. The
problems induced by this are not just theoretical; they will utterly destroy
permutation testing of many trading systems. Real markets do not behave this
way.
The solution to this problem is easy, though a bit messy. We split the
(relatively large) intra-bar changes and the (mostly tiny) inter-bar changes into
two separate series and permute each separately. When we rebuild the permuted
series, we get each new bar in two steps. First, we use the permuted inter-bar
change to move from the close of one bar to the open of the next. Then we use
the permuted intra-bar change to move from the open to the close, picking up the
high and low along the way.
In the code that appears soon, understand that the permutation routines will
be called with the first bar on which a trade decision is possible. If there is a
lookback, we assume that this has been taken into account.
The code that prepares for permutation is straightforward. As usual, we
assume that all prices are actually log prices. If they are the real prices, we must
use ratios rather than differences; otherwise, the algorithm is the same.
The first bar is the “base” bar, and it does not change at all. Subsequent bars
will be generated from its close. As we will see when we examine the code, the
close of the last bar will also remain unchanged. For each bar, rel
_
open is the
gap between the prior close and the current open. The high, low, and close of the
current bar are all relative to the open of the bar.
void prepare
_permute (
int nc , double *open , // Number of bars
// Input of nc log
prices
double *high ,
double *low ,
double *close ,
double *rel
_
open , computed changes
double *rel
_
double *rel
_
double *rel
high ,
low ,
close
_
)
// Work area; returns
{
int icase ;
for (icase=1 ; icase<nc ; icase++) {
rel
_
open[icase-1] = open[icase] -
close[icase-1] ;
rel
_
high[icase-1] = high[icase] - open[icase]
;
rel
_
low[icase-1] = low[icase] - open[icase] ;
rel
_
close[icase-1] = close[icase] -
open[icase] ;
}
}
The permutation routine has a parameter, preserve
_
OO, that needs special
explanation. The vast majority of example trading systems in this book are based
on a single price series, with trades being executed as market-on-close to the
close of the next bar (possibly continuing on to the close of a subsequent bar).
This can sometimes give slightly optimistic results, not to mention that it is
tinged with a hint of being unrealistic and unobtainable in real life. A more
conservative approach is to open a trade on the open of the bar following the
trade decision. If we are partitioning the total return of the trading system as
described beginning on page **294** and we want to be squeaky clean about how we
define the total trend across the test period, we must define the trend by the
change from the first open after the earliest possible decision to the last open,
and we need this change to be the same for all permutations. (This is probably
excessively cautious, but it’s easy to do, so we might as well.) For this difference
to remain the same for all permutations, we must not allow the first close-to-
open change or the last open-to-close change to take part in the permutation.
Setting preserve
_
OO to any nonzero number does this. With this in mind, here is
the permutation code. First we shuffle the close- to-open changes.
void do
_permute (
int nc , // Number
of cases
int preserve
_
OO , // Preserve next
open-to-open (vs first open to last close)
double *open , // Returns nc
shuffled log prices
double *high ,
double *low ,
double *close ,
double *rel
_
open , // Work area; input
of computed changes
double *rel
_
high ,
double *rel
_
low ,
double *rel
close
_
)
{
int i, j, icase ;
double dtemp ;
if (preserve
_
OO)
preserve
_
OO = 1 ;
i = nc-1-preserve
_
OO ; be shuffled
// Number remaining to
while (i > 1) { // While at
least 2 left to shuffle
j = (int) (unifrand() * i) ;
if (j >= i) // Should
not happen, but be safe
j = i - 1 ;
--i ;
dtemp = rel
_
open[i+preserve
_
OO] ;
rel
_
open[i+preserve
_
OO] =
rel
_
open[j+preserve
_
OO] ;
rel
_
open[j+preserve
_
OO] = dtemp ;
} // Shuffle the close-to-open changes
In the previous code, we note the effect of preserve
_
OO. If it is input
zero, we shuffle all nc–1 close-to-open inter-bar changes. But if it is one, we
have one less change to shuffle, and we offset all shuffling by one. This
preserves the first inter-bar close-to-open change, meaning that the open of the
second bar, which is the opening price of the first possible “next bar” trade,
remains unchanged for all permutations.
Next we shuffle the intra-bar changes. We must shuffle the high, low, and
close identically to preserve the high and low bounding the open and close. The
effect of preserve
_
OO is slightly different here. Instead of preserving the first
close-to-open change, it preserves the last open-to-close change. Because the last
close is always preserved, allowing the last bar’s open-to-close difference to
change would change the open of the last bar.
i = nc-1-preserve
_
OO ; // Number remaining to be
shuffled
while (i > 1) { // While at least 2 left
to shuffle
j = (int) (unifrand() * i) ;
if (j >= i) // Should never happen,
but be safe
j = i - 1 ;
--i ;
dtemp = rel
_
high[i] ;
rel
_
high[i] = rel
_
high[j] ;
rel
_
high[j] = dtemp ;
dtemp = rel
_
low[i] ;
rel
;
1] ;
}
rel
_
low[i] = rel
_
low[j] ;
rel
_
low[j] = dtemp ;
dtemp = rel
_
close[i] ;
rel
_
close[i] = rel
_
close[j] ;
rel
_
close[j] = dtemp ;
} // Shuffle the open-to-close changes
Rebuilding the price history using the shuffled changes is trivial.
_
for (icase=1 ; icase<nc ; icase++) {
open[icase] = close[icase-1] +
open[icase-1] ;
high[icase] = open[icase] + rel
_
high[icase-1]
low[icase] = open[icase] + rel
_
low[icase-1] ;
close[icase] = open[icase] + rel
_
close[icase-
}
Example: P-Value and Partitioning
The file **MCPT**
_
**TRN**.**CPP** contains an example of computing a training p-value
(pages **286** and **291**) and total return partitioning (page **294**) for a primitive
moving-average crossover system trained on **OEX**. The program is executed
with the following command:
**MCPT**
_
**TRN** MaxLookback Nreps FileName
Let’s break this command down:
MaxLookback: Maximum moving-average lookback
Nreps: Number of **MCPT** replications (hundreds or thousands)
FileName: Name of market file (**YYYYMMDD** Price)
The following Figures 7-1 and 7-2 is the output of this program when
executed with the S&P **100** and S&P **500** indexes. It’s fascinating what
extremely different results are obtained. Please refer to the previously cited
pages for detailed explanations of the computed quantities. An overview of the
program’s code begins on the next page.
Figure 7-1 Output of the **MCPT**
_
**TRN** program for **OEX**
Figure 7-2 Output of the **MCPT**
_
**TRN** program with **SPX**
The moving-average crossover system is the same as we have seen in prior
examples. It computes short-term and long-term moving averages (where the
lookbacks are optimizable) and takes a long position when the short term MA is
above the long-term MA, and it takes a short position when the reverse is true.
We focus here on computation of the performance figures.
First, we compute the total trend and divide it by the number of individual
returns to get the trend per individual return. Remember that the first price on
which a valid trade decision can be made is the “basis” price, with permutation
beginning on the change from it to the next bar. By starting at this point, we
ensure that all possible individual trade returns are subject to permutation, and
we also guarantee that no change prior to a possible trade can be permuted into
the mix, which could change the total trend. Then we call the preparation routine
listed on page **299** to compute and save the price changes.
trend
_per
_
return=(prices[nprices-1]-
prices[max
_
lookback-1]) / (nprices-max
_
lookback) ;
prepare
_permute ( nprices-max
_
lookback+1 ,
prices+max
_
lookback-1 , changes ) ;
In the **MCP** loop, we permute on all but the first pass. We will need the
number of long and short returns from the optimized system to compute the
trend component. For the first, unpermuted trial save all “original” results.
for (irep=0 ; irep<nreps ; irep++) {
if (irep) // Shuffle
do
_permute ( nprices-max
_
lookback+1 ,
prices+max
_
lookback-1 , changes ) ;
opt
_
return = opt
_params ( nprices , max
lookback
_
, prices ,
&short
_
lookback , &long_
lookback , &nshort , &nlong ) ;
trend
_
component = (nlong - nshort) *
trend
_per
_
return ; // Equation 7-1 on page **297**
if (irep == 0) { // This is the
original, unpermuted trial
original = opt
_
return ;
original
trend
_
_
component = trend
_
component ;
original
_
nshort = nshort ;
original
_
nlong = nlong ;
count = 1 ; // Algorithm on Page **291**
mean
_
training_
bias = 0.0 ;
}
else { // This is a permuted trial
training_
bias = opt
return - trend
_
_
component
; // Equation 7-3 on page **297**
mean
_
training_
bias += training_
bias
; // Average across permutations
if (opt
return >=
_
original) //
Algorithm on Page **291**
++count ;
}
} // For all replications
mean
_
training_
bias /= (nreps - 1)
; // First trial was
unpermuted
unbiased
_
return = original - mean
_
training_
bias
; // Equation 7-4 on page **297**
skill = unbiased
_
return - original
trend
_
_
component
; // Equation 7-5 on page **297**
Example: Training with Next Bar Returns
The file **MCPT**
_
**BARS**.**CPP** contains a demonstration program that does the
same p-value computation and total return partitioning as the prior example.
However, instead of using a single price series, the price data is day bars
(although it could be bars of any length). Moreover, it uses a more conservative
method for computing returns. The return of each trade decision is the (log) price
change from the open of the next bar to the open of the following bar. Finally, it
is a different trading system, a simple mean-reversion strategy rather than
moving-average crossover. The program is invoked with the following
command:
**MCPT**
_
**BARS** MaxLookback Nreps FileName
Let’s break this command down:
MaxLookback: Maximum moving-average lookback
Nreps: Number of **MCPT** replications (hundreds or thousands)
FileName: Name of market file (**YYYYMMDD** Open High Low Close)
Figure 7-3 shows the output of this program for the S&P **100** index, and
Figure 7-4 shows it for S&P **500**.
Figure 7-3 Output of the **MCPT**
_
**BARS** program for **OEX**
Figure 7-4 Output of the **MCPT**
_
**BARS** program for **SPX**
As with the prior example, we see a profound difference in performance in
these two markets. It’s not at all surprising that, in any market, a primitive trend-
following system such as MA **XOVER** would perform very differently from a
mean reversion system. But what is surprising is how incredibly differently they
perform in these two markets that would seem to be similar in composition. In
fact, the p-value for **SPX** is almost 1.0, a stunning value. Clearly, this market is
anti-mean-reversion! This would certainly square with this market’s trend-
following p-value of 0.**001**, the minimum possible with **1000** replications, an
equally stunning value. But wow. I mean, wow. The only other consideration is
that the **SPX** market used in this example starts its history several decades
earlier(**1962**) than the **OEX** market (**1982**), so earlier data may play a role.
Plotting an equity curve of each system in each market would be most revealing.
If you beat me to it, send me an email.
Because this trading system uses a slightly different method for computing
returns, it’s worth examining both the system itself and the associated **MCPT**
code. We begin with the trading system. It computes a simplistic long-term trend
as the current close minus the close a user-specified fixed number of bars earlier.
This is typically a large number, a thousand or several thousand bars. It also
looks at the current price drop, the (log) price of the prior bar minus that of the
current bar. If the long-term trend is above an optimizable threshold and the
price drop is also above its own optimizable threshold, a long position is taken
for the next bar. The philosophy behind this system is that a sudden sharp drop in
the price of an uptrending market is a temporary aberration that will be corrected
on the next bar. Here is the calling convention for this subroutine:
double opt
_params ( profit starting at lookback
int ncases , // Returns total log
// Number of log
prices
int lookback , // Lookback for
long-term rise
double *open , // Log of open
prices
double *close , // Log of close
prices
double *opt
_
rise , // Returns optimal
long-term rise threshold
double *opt
_
drop , // Returns optimal
short-term drop threshold
int *nlong // Number of
long returns
)
We will use best
_perf to keep track of the best total return. The
outermost pair of loops try a large variety of thresholds for the long-term uptrend
and the immediate price drop.
best
_perf = -1.e60
; // Will be best
performance across all trials
for (irise=1 ; irise<=50 ; irise++)
{ // Trial long-term rise
rise
_
thresh = irise * 0.**005** ;
for (idrop=1 ; idrop<=50 ; idrop++) { Trial short-term drop
drop_
thresh = idrop *
.**0005** ;
//
Given this pair of trial thresholds, we pass through the valid market history
and cumulate the total return. We also count the number of long positions taken,
because we will need this to compute the trend component. We begin this
cumulation at the lookback distance, as we will need this much history to
compute the long-term trend. We must stop two bars before the end of the
dataset because the conservatively computed return for a trade is the (log) price
change from the open of the bar after the decision is made, to the open of the
following bar.
total
_
return = 0.0 ; // Cumulate total
return for this trial
nl = 0 ; // Will
count long positions
for (i=lookback ; i<ncases-2 ; i++)
{ // Compute performance across history
rise = close[i] - close[i-lookback]
; // Long-term trend
drop = close[i-1] - close[i]
; // Immediate price drop
if (rise >= rise
_
thresh && drop >=
drop_
thresh) {
ret = open[i+2] - open[i+1]
; // Conservative return
++nl ;
}
else
ret = 0.0 ;
total
_
return += ret ;
} // For i, summing performance for
this trial
All that remains is the trivial bookkeeping task of keeping track of the
optimal parameters and their associated results.
if (total
return > best
_
_perf) { // Did
this trial param set break a record?
best
_perf = total
_
return ;
*opt
rise = rise
_
_
thresh ;
*opt
_
drop = drop_
thresh ;
*nlong = nl ;
}
} // For idrop
} // For irise
return best
_perf ;
}
The general actions of the permutation tests are identical to those in the prior
section. However, because we are computing returns using the open of the next
two bars, offsets are a little different. The definition of lookback in this
system is also slightly different from the max
_
lookback of the prior system,
so that also introduces some differences. Consider the trend per return and the
preparation routine. The first trade decision can be made at the bar with index
lookback, so we call prepare
_permute() with this offset to all four price
arrays. This bar will remain fixed; permutation starts at the next bar, which is
also where trade returns start. A total of nprices–lookback bars are
available to the permutation routine. The first possible trade can open at bar
lookback+1 and close at the open of the last bar, nprices–1.
trend
_per
_
return = (open[nprices-1] -
open[lookback+1]) / (nprices - lookback - 2) ;
prepare
_permute ( nprices-lookback ,
open+lookback , high+lookback ,
low+lookback , close+lookback ,
rel
_
open , rel
_
high , rel
_
low , rel
_
c lose ) ;
All remaining computations are identical to what we saw in the prior section,
so there is no point in repeating them here. And of course, the complete source
code is available in **MCPT**
**BARS**.**CPP**._
Example: Permuting Multiple Markets
On page **179** we examined the program whose code is available in
**CHOOSER**.**CPP** . In that section we focused on how to use nested walkforward
to get out-of-sample returns in a selection-bias situation. Permutation was
ignored then. Now we return to that program, focusing this time on the
permutation test that evaluates the probability that **OOS** results at least as good
as those obtained could have been obtained by random good luck. Note that this
is not the selection-bias-permutation algorithm shown on page **292**. No example
of that algorithm is given in this book, as it is a straightforward extension of the
simpler algorithm and well documented in the flow chart. Numerous source code
examples of this algorithm can be found in my book Data Mining Algorithms in
C++. The real purpose of this section is to provide an example of permuting
multiple markets simultaneously to evaluate a multiple-market trading system, as
well as demonstrating how permutation should be split into segments in a
walkforward situation that contains selection.
The multiple-market permutation routines were discussed in detail starting
on page **301**, and it wouldn’t hurt to review that section. For convenience, here is
the calling list for prepare
_permute(); that for do
_permute() is
identical:
void prepare
_permute (
int nc , cases total (not just starting at offset)
int nmkt , // Number of
// Number of
markets
int offset , case to be permuted (>0)
double **data , price matrix
double **changes computed changes
)
// Index of first
// Input of nmkt by nc
// Work area; returns
We already saw an example of splitting market history into permutation
groups using a simple walkforward situation. Our motivation was the fact that
the initial training fold does not appear in any **OOS** fold in the original,
unpermuted run. Thus, we must ensure that this is also the case for the permuted
trials, in case that initial period contains data that is unusual in trend, volatility,
or some other important property. We must not allow any unusual data to leak
into a permuted **OOS** fold.
The situation is more complex when we are doing nested walkforward, as in
the **CHOOSER** program. Now we have two **OOS** folds to deal with. These are
the two quantities we will have to consider:
IS
_
n: Although no actual training occurs at the outer level of walkforward
nesting in **CHOOSER**, this is the number of cases that play the role of
“training set” in the program. Of particular importance in the context of
permutation is the fact that in the original, unpermuted trial, none of these
cases will ever appear in either level of **OOS** fold results. Thus, these cases
must never be allowed to permute into future **OOS** folds and potentially
contaminate them with unusual changes.
**OOS1**
n: This is the number of cases in the inner level of walkforward **OOS**
_
folds. The outer **OOS** folds, those in which we are ultimately interested
because they are fully **OOS**, begin after IS
n+**OOS1**
n cases. The cases in
_
_
the first inner walkforward **OOS** fold, those from IS
_
n up to (but not
including) IS
n+**OOS1**
_
_
n, must not permute into the outer folds, because
they are not there in the unpermuted trial.
With these thoughts in mind, we split the market history into three separate
segments and permute each separately. It is an open question as to the wisdom
(or lack thereof) of permuting the first “training” fold in general. I choose to do
so here, primarily for pedagogical purposes, though I am not aware of any pros
or cons. My own opinion, unsupported by any facts, is that on average it makes
no difference one way or the other.
The first line of the following code prepares to permute this first “training”
fold, perhaps unnecessarily. The second line handles the first inner **OOS** fold,
and the last line handles the outer **OOS** fold area, which is our area of ultimate
interest. For permutation, the do
_permute() routine is called with the same
parameters. All other operation is identical to what we have seen before.
prepare
_permute( IS
_
n, n
_
markets, 1 , market
close
_
, permute
_
work ) ;
prepare
_permute( IS
n+**OOS1**
_
_
n, n
_
markets , IS
_
n,
market
_
close , permute
_
work ) ;
prepare
_permute( n
_
cases, n
_
markets , IS
n+**OOS1**
_
_
n,
market
_
close , permute
_
work);
We now reproduce the output of this program that was presented earlier,
before permutation tests had been discussed. The meanings of the computed p-
values should now be clear.
Mean = 8.**7473**
**25200** * mean return of each criterion, p-value, and
percent of times chosen...
Total return 17.**8898** p=0.**076** Chosen 67.8
pct
Sharpe ratio 12.**9834** p=0.**138** Chosen 21.1
pct
Profit factor 12.**2799** p=0.**180** Chosen 11.1
pct
**25200** * mean return of final system = 19.**1151**
p=0.**027**
Observe that the p-values for the three individual performance criteria are
only moderately significant, with Total return being the best at 0.**076**. But for the
final algorithm that uses nested walkforward to test not only market selection but
performance criterion selection as well, the p-value of 0.**027** is quite impressive.