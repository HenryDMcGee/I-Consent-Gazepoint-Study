library(sciplot)
library(ez)
library(psych)
library(reshape)
library(ggplot2)

#subj,cond,stim,ANN
df <- read.csv("anns.csv") # open data

mdf <- melt(df, id=c("subj","cond","stim"))
stimmeans <- cast(mdf, stim~variable, mean)

#subj,cond,stim,ann
# calculate anova
#ezANOVA(data=df, dv=ann, wid=subj, within=cond, type=3)
df$subj <- factor(df$subj)
df$cond <- factor(df$cond)
df$stim <- factor(df$stim)
attach(df)
#summary(aov(ann ~ (cond * stim) + Error(subj/cond), df))
#summary(aov(nni ~ (cond * stim) + Error(subj/cond), df))
# if there's no condition, just use simple one-way ANOVA
summary(aov(ann ~ stim, df))
summary(aov(nni ~ stim, df))
detach(df)

#pairwise.t.test(df$ann, df$cond, p.adj="bonferroni")
#describeBy(df$ann, group=df$cond)
describeBy(df$ann, group=df$stim)

#pairwise.t.test(df$nni, df$cond, p.adj="bonferroni")
#describeBy(df$nni, group=df$cond)
describeBy(df$nni, group=df$stim)

plotName = "./nni-stim.pdf"
pdf(plotName,family="NimbusSan",useDingbats=FALSE)
bargraph.CI(stim, nni, group = NULL, data = df,
            split = FALSE,
            col = c("#f0f0f0","#bdbdbd","#636363"),
            angle = c(45,45,45),
            density = c(60,60,60),
            lc = TRUE,
            uc = TRUE,
            legend = FALSE,
            ncol = 1,
            leg.lab = NULL,
            x.leg = 6.2,
            y.leg = 2.4,
            cex.leg = 1.2,
#           ylim = c(0,1.0),
            xlab = "Stimulus",
            ylab = "Mean NNI z-score",
            cex.lab = 1.3,
            cex.names = 1.3,
            main = "NNI z-score vs. Stimulus"
)
dev.off()
embedFonts(plotName, "pdfwrite", outfile = plotName,
  fontpaths =
  c("/sw/share/texmf-dist/fonts/type1/urw/helvetic",
    "/usr/share/texmf/fonts/type1/urw/helvetic",
    "/usr/local/teTeX/share/texmf-dist/fonts/type1/urw/helvetic",
    "/opt/local/share/texmf-texlive/fonts/type1/urw/helvetic",
    "/usr/share/texmf-texlive/fonts/type1/urw/helvetic",
    "/usr/local/texlive/texmf-local/fonts/type1/urw/helvetic"))
