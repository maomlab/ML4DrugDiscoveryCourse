# Bayesian Modeling with Stan
In this lab you will fit Bayesian models to for a cell-count dataset.

### Learning Objectives

* Practical experience with and thinking about Bayesian modeling including prior, likelihood, and posterior
* Familiarity with Stan-based Bayesian modeling, and related tools

### Data and problem background
Cells adhere to a range different extra-cellular matrix proteins. To measure this, there is an experimental
where a plate is prepared different combinations of 9 ECM proteins in spots, cells are cultured on the plate
and then washed off, the number of cells in each spot are counted to quantify the adherence.

In the provided data, tendon cells from wildtype and AMPK knockout mice were collected and tested for their
differential adherence. These data were collected by Dr. LeeAnn Flowers in the Abraham lab at the University
of Michigan.


### References

  * Statistical Rethinking 2nd Ed. by Richard McElreath,
    [book website](https://github.com/rmcelreath/stat_rethinking_2024)
    The e-book is available through the university library

  * [Bayesian Workflow](https://arxiv.org/abs/2011.01808) by Gelman et al., 2020, manuscript is a
    an overview of the strategy for using Bayesian modeling to develop statistical modeling

  * [Stan Documentation](https://mc-stan.org/) website for the Stan ecosystem

## Steps

### 1 Install Stan
Stan is a Bayesian modeling framework that includes inference engines, a model specification language
and an ecosystem of tools for Bayesian modleing. In R there are two main interfaces, ` CmdStanR` and `rstan`.
`CmdStanR` is generally faster and more up-to-date, but `rstan` is better integrated with `R`. Here we'll
use `CmdStanR`. See the [Getting Started with CmdStanR](https://mc-stan.org/cmdstanr/articles/cmdstanr.html).

    install.packages(
       "cmdstanr",
       repos = c('https://stan-dev.r-universe.dev', getOption("repos")))
    cmdstanr::install_cmdstan()
    file <- file.path(cmdstan_path(), "examples", "bernoulli", "bernoulli.stan")
    mod <- cmdstan_model(file)

Install the [BRMS](https://paulbuerkner.com/brms/) package that is used for Bayesian regression modeling

    # used for fitting regression models with Stan
    install.packages("brms")

    # used for doing leave-one-out cross validation model evaluation and model comparison
    install.packages("loo")

    # help with working with posterior samples
    install.packages("posterior")

    # visualizing and model fits
    install.packages("bayesplot")
    install.packages("shinystan")

Set global parameters in each script that uses these packages:

    options(brms.backend = "cmdstanr")
    options(mc.cores = 4)

### 2 Gather and inspect data for adhesion assay
In the excel spreadsheet in the data folder, on the second tab, the data consists of the cell counts
for each spot, the Genotype (where 1 is wildtype and 0 is AMPK knockout), and the remaining columns
indicate the presense or absense of the 9 different ECM proteins in each spot. So for example, the first
row indicates that for the spot with just the Col1, 99 tendon cells from the wildtype mouse were measured
to adhere.

Load this data and plot a histogram of the counts.

### 3 Fit A Bayesian Regression Model
Use BRMS to fit a poisson model (`model1`) to the data using the `brms::brm()` function. Using the R formula syntax,
have the response be `Counts` and then each of `Genotype` and each ECM protein be an linear covariate
predictor of the response. Since the response is counts, set `family = poisson` argument to `brm(...)`.
Poisson regression is a type of generalized linear regression with with a `log` link function.

#### Check the model specification

and Stan model code for the model,

    model1$model

Check that the target log-likelyhood for makes sense (e.g. what does [poisson_log_glm_lpmf](https://mc-stan.org/docs/functions-reference/unbounded_discrete_distributions.html#poisson-log-glm) mean?


#### Check the model has converged

When printing the summary

    model1

does it give any [warnings](https://mc-stan.org/learn-stan/diagnostics-warnings.html) about divergences?
This can happen if there is a mismatch between the prior and the data
and simulation gets stuck. It this happens, you can increase sampling by adding to the `brm()`:

    control = list(adapt_delta = 0.99, max_treedepth = 12)

For each parameter, the `Rhat` column should be close to `1` and the `bulk_ESS` and `tail_ESS` give the
effective number of samples in the bulk and tail of the the distributions, and generally if more than 1000
than this is not a concern.


#### Add a prior
Without specifying a prior, BRMS uses a flat prior. To see this, check

    model1$prior

To specify valid, but [weakly informative priors](https://github.com/stan-dev/stan/wiki/prior-choice-recommendations),
you can specify them like this

    prior_main <- c(
        brms::prior(normal(4.5, 3), class = "Intercept"),
        brms::prior(normal(0, 3), class = "b", coef = "Genotype")
        ...)

then pass this to `brm(..., prior = prior_main)`. The `class = "Intercept"` here is for the model intercepte
the class `"b"` here is for the parameters associated with the linear coefficients. The log of the mean of the
Counts is a reasonabl center for the Intercept term.

### 4 Fit alternative models
Beyond the baseline `model1`, To fit more complex models that may fit the data better, fit `model2`
that inclues interaction terms, `model3` that fits a negative binomial model instead of a poisson model, and `model4`
that fits the interaction term and negative binomial link.

To fit the interaction term, instead of having the `Counts ~ Genotype + Col1 + ...` for the formula,
instead have `Counts ~ Genotype * (Col1 + ...)` in the formula. And, add priors for the interaction terms
that can then be combined with the `prior_main` in the `brm` model specification. We can define them outside
of the `brm(...)` call, so we can include them in both `model2` and `model4` without redundant.

    prior_interaction <- c(
        brms::prior(normal(0, 3), class = "b", coef = "Genotype:Col1"),
        ...)

To fit a negative binomial model instead of Poisson model for the response, you can set
`brms(..., family = brms::negbinomial(), ...)`. To explore the difference between the poisson model and the
negative binomial model, check out it in the [Distribution Explorer](https://distribution-explorer.github.io/discrete/negative_binomial.html). Then since the negative binomial has a shape parameter, it also needs a prior,

    prior_nb <- c(
        # this is the brms default prior for the negative binomial family shape param
        brms::prior(inv_gamma(0.4, 0.3), class = "shape", lb = 0))

the shape parameter controls the overdispersion, as `Var(Y) = mu + mu^2/shape`, so as shape gets bigger,
the overdispersion factor gets smaller, so in the limit of `shape == Inf`, then `Var(Y) = mu`, which is essentially
the Poisson model, and if `shape < Inf`, then the the response valeus have higher variance than one would expect
at random. In thise if there was some random grouping or common reasons why cells stick to a spot beyond
beyond happening independently by chance.

Fit each of the four models, which should take a few seconds each, and inspect them to make sure it makes some sense.

### 5 Analyze the model fits
Here we'll check the model fits by comparing the fit of different models and interpreting the
marginal posterior distirbutions for each parameter.

### Check the fit quality using leave-one-out cross validation.
Use the `brms::add_criterion(...)` function to compute leave-one-out cross validation like this:

    model1 <- model1 |> brms::add_criterion("loo", re_loo = TRUE)
    model1$criteria$loo

This computes an approximate LOO for data points that are fit well by the model, the `re_loo=TRUE` argument,
means to re-compute the model for outliers. Seek the LOO [FAQ](https://users.aalto.fi/~ave/CV-FAQ.html) for
good background

To interpret the output of loo, there are two things to look at, the `elpd_loo` is the "expected log-likelihood
under the posterior density" and more positive numbers means a better fit. And second, the Pareto
k diagnostic values give an indication of if there are outliers to the model, wehre generally less than
0.7 considere good, (0.7, 1] is bad and greater than 1 is very bad.

You can compare the fit of models on the same dataset based on the `elpd_loo`. Pass a named list
of loo objects to `loo::loo_compare(...)` like this

    model_comparison <- loo::loo_compare(list(
        Additive = model1$criteria$loo,
        Interaction = model2$criteria$loo,
        Additive_NB = model3$criteria$loo,
        Interaction_NB = model4$criteria$loo))

    # print the summary
    model_comparison

    # save it to disk etc.
    model_comparison |> as.data.frame() |> readr::write_tsv(...)


#### Plot data
There are a bunch of summary and diagnostic plots that can help to communicate and interpret

    shinystan::launch_shinystan(model)

Look throught the DIAGNOSE, ESTIMATE, and EXPLORE tabs.

To plot the posterior parameter estimates, you can use `bayesplot`


    plot <- bayesplot::mcmc_areas(
        x = model,
        pars = bayesplot::vars(-lprior, -lp__, -Intercept, -shape),
        prob = 0.8) +
        ggplot2::theme_bw() +
        ggplot2::ggtitle(
          label = paste0("Posterior distributions"),
          subtitle = "with medians and 80% intervals") +
        ggplot2::geom_vline(
          xintercept = 0,
          color = "darkgray",
          linewidth = 1.4) +
        ggplot2::scale_x_continuous(
            "Fold Change Nuclei Count",
            breaks = log(c(0.01, 0.1, 1, 10, 100)),
            labels = c("1%", "10%", "1x", "10x", "100x"))

    # this is an optional trick to move the vline behind the data
    plot <- plot |>
        gginnards::move_layers("GeomVline", position = "bottom")


#### Test hypotheses
Similar to frequentist statistics it is still possible to test (hypotheses)[https://paulbuerkner.com/brms/reference/hypothesis.brmsfit.html], the main difference is since we have samples from the posterior, if we want to say test if a parameter is begger than 0, we can look at the draws from the posterior and ask what fraction
have the parameter above 0? This easy to do like this.

    model |> brms::hypothesis(c(
       "Col1 > 0",
       "Laminin > 0",
       ...)


## What to turn in

  * For the 4 models, what model fits the best? Is there support from the model comparison to fit
    interaction terms or use negative binomial regression?

  * How sensitive is the analysis to the weakly informative priors? If you misspecify them, (e.g. by setting the
    mean of the normal very far from the estimated value, what happens to the model fit?

  * What is one thing you noticed in the shinystan for one of your models?

  * A brief summary of the model fit and what the significant findings are along with the plot of the posterior
    estimates
