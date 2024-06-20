library(sciplot)
library(ez)
library(psych)
library(reshape)
library(ggplot2)

source("lrheatmap.R") # load custom functions
source("TMSP.R") # load custom functions

args <- commandArgs(trailingOnly = TRUE)
#print(args)

xtiles <- as.integer(args[1])
ytiles <- as.integer(args[2])
print(sprintf("xtiles = %d, ytiles = %d\n",xtiles,ytiles))

M <- zeroTM(xtiles,ytiles)

df <- read.csv("aois.csv") # open data

ddf <- df[which(df$cond == "p1"), ] # select condition
ddf
M_p1 <- TransMatrix(M,data=ddf,
                    AOInamesVar="AOI",
                    SubjectsVar="subj",
                    FixOrderVar="order")
M_p1 <- M
en_p1 <- TransEntropy(M,data=ddf,
                    AOInamesVar="AOI",
                    SubjectsVar="subj",
                    FixOrderVar="order")
en_p1 <- TMentrop
sen_p1 <- StationaryEntropy(M,data=ddf,
                    AOInamesVar="AOI",
                    SubjectsVar="subj",
                    FixOrderVar="order")
sen_p1 <- STentrop
TransPlot2(transMatrix=M_p1,
           plotName="TM_p1.pdf",
           plotColors=brewer.pal(9,"Oranges"),
           annColor='black')
#          plotColors=brewer.pal(4,"Greys"),
#          annColor='#252525')

M <- zeroTM(xtiles,ytiles)

ddf <- df[which(df$cond == "p2"), ] # select condition
M_p2 <- TransMatrix(M,data=ddf,
                    AOInamesVar="AOI",
                    SubjectsVar="subj",
                    FixOrderVar="order")
M_p2 <- M
en_p2 <- TransEntropy(M,data=ddf,
                    AOInamesVar="AOI",
                    SubjectsVar="subj",
                    FixOrderVar="order")
en_p2 <- TMentrop
sen_p2 <- StationaryEntropy(M,data=ddf,
                    AOInamesVar="AOI",
                    SubjectsVar="subj",
                    FixOrderVar="order")
sen_p2 <- STentrop
TransPlot2(transMatrix=M_p2,
           plotName="TM_p2.pdf",
           plotColors=brewer.pal(9,"Oranges"),
           annColor='black')
#          plotColors=brewer.pal(4,"Greys"),
#          annColor='#252525')

# this should be normalized stationary entropy
#M_p1
SE_p1 <- H_s(M_p1)
SE_p1$eta
SE_p1$sdist
#M_p2
SE_p2 <- H_s(M_p2)
SE_p2$eta
SE_p2$sdist

# Note: entropy is computed as the empirical entropy, estimated via maximum
#	likelihood, bias-corrected by applying the Miller-Madow correction
#	to the empirical entropy
#en_p1
#en_p2
con_p1 <- c(rep("p1",length(en_p1$Subject)))
con_p2 <- c(rep("p2",length(en_p2$Subject)))

# construct new data frame
Entropy <- c(en_p1$Entropy, en_p2$Entropy)
Subject <- c(en_p1$Subject, en_p2$Subject)
Task <- c(con_p1, con_p2)
d <- data.frame(Entropy, Subject, Task)
d

# calculate anova
#ezANOVA(data=d, dv=Entropy, wid=Subject, within=Task, type=3)
d$Subject <- factor(d$Subject)
d$Task <- factor(d$Task)
attach(d)
#H.aov <- aov(Entropy ~ (Subject * Task) + Error(Subject / Task), d)
#H.aov <- aov(Entropy ~ (Subject * Task) + Error(Subject), d)
H.aov <- aov(Entropy ~ Task + Error(Subject), d)
summary(H.aov)
detach(d)

t.test(d$Entropy ~ d$Task)
pairwise.t.test(d$Entropy, d$Task, p.adj="bonferroni")
describeBy(d$Entropy, group=d$Task)
ddf_p1 = d$Entropy[which(d$Task == "p1")]
ddf_p2 = d$Entropy[which(d$Task == "p2")]
power.t.test(power=.95,sig.level=.05,sd=max(sd(ddf_p1),sd(ddf_p2)),delta=abs(mean(ddf_p1)-mean(ddf_p2)))

pdf("./entropy.pdf",family="NimbusSan",useDingbats=FALSE)
bargraph.CI(Task, Entropy, group = NULL, data = d,
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
#           ylim = c(0,0.5),
            ylim = c(0,1.0),
            xlab = "Task Type",
            ylab = "Mean Normalized Transition Entropy (bits/transition with SE)",
            cex.lab = 1.3,
#           names.arg = c("0", "1"),
            names.arg = c("VE-NW", "VE-W"),
            cex.names = 1.3,
            main = "Normalized Transition Entropy vs. Task Type"
)
dev.off()
embedFonts("./entropy.pdf", "pdfwrite", outfile = "./entropy.pdf",
  fontpaths =
  c("/sw/share/texmf-dist/fonts/type1/urw/helvetic",
    "/usr/share/texmf/fonts/type1/urw/helvetic",
    "/usr/local/teTeX/share/texmf-dist/fonts/type1/urw/helvetic",
    "/usr/share/texmf-texlive/fonts/type1/urw/helvetic",
    "/usr/local/texlive/texmf-local/fonts/type1/urw/helvetic"))

# construct new data frame
SEntropy <- c(sen_p1$SEntropy, sen_p2$SEntropy)
Subject <- c(sen_p1$Subject, sen_p2$Subject)
Task <- c(con_p1, con_p2)
d2 <- data.frame(SEntropy, Subject, Task)
d2

t.test(d2$SEntropy ~ d2$Task)
describeBy(d2$SEntropy, group=d2$Task)

pdf("./sentropy.pdf",family="NimbusSan",useDingbats=FALSE)
bargraph.CI(Task, SEntropy, group = NULL, data = d2,
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
#           ylim = c(0,0.5),
            ylim = c(0,1.0),
            xlab = "Task Type",
            ylab = "Mean Normalized Stationay Entropy (bits/transition with SE)",
            cex.lab = 1.3,
#           names.arg = c("0", "1"),
            names.arg = c("VE-NW", "VE-W"),
            cex.names = 1.3,
            main = "Normalized Stationary Entropy vs. Task Type"
)
dev.off()
embedFonts("./sentropy.pdf", "pdfwrite", outfile = "./sentropy.pdf",
  fontpaths =
  c("/sw/share/texmf-dist/fonts/type1/urw/helvetic",
    "/usr/share/texmf/fonts/type1/urw/helvetic",
    "/usr/local/teTeX/share/texmf-dist/fonts/type1/urw/helvetic",
    "/usr/share/texmf-texlive/fonts/type1/urw/helvetic",
    "/usr/local/texlive/texmf-local/fonts/type1/urw/helvetic"))
