#!/usr/bin/env python

"""
For each model check outputs are sensible...Varible climate experiment

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (26.03.2014)"
__email__ = "mdekauwe@gmail.com"

import sys, os, glob
import pandas as pd
import cPickle as pickle
import numpy as np
import plot_settings as ps
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import brewer2mpl

class FaceInterface(object):
    def __init__(self, fdir):

        self.model_list = ["CABL","CLM4","CLMP","GDAY","LPJX","OCNX","SDVM"]

    def get_data(self):

        df = pd.read_pickle(os.path.join(fdir, "models_output.pkl"))
        return df, self.model_list

def setup_fig():

    plt.rcParams['legend.fontsize'] = 8
    plt.rcParams['lines.linewidth'] = 1.0
    plt.rcParams['xtick.labelsize'] = 10.0
    plt.rcParams['ytick.labelsize'] = 10.0
    plt.rcParams['axes.labelsize'] = 10.0
    plt.rcParams['font.size'] = 10.0
    plt.rcParams['axes.labelsize'] = 10.

def main(fdir, ofdir, exp):

    F = FaceInterface(fdir)
    (df, model_list) = F.get_data()

    pdf = PdfPages(os.path.join(ofdir, "check_outputs_%s.pdf" % (exp)))

    #colours = brewer2mpl.get_map('set1', 'qualitative', 6).mpl_colors
    #colours[5] = "gold"
    colour_list = ps.get_colour_list(8)

    #
    # ET = T + ES + EC
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("ET = T+ES+EC")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()
            ET = df[model,treat,exp].groupby("YEAR").ET.sum()
            T = df[model,treat,exp].groupby("YEAR").T.sum()
            ES = df[model,treat,exp].groupby("YEAR").ES.sum()
            EC = df[model,treat,exp].groupby("YEAR").EC.sum()

            X = ET
            Y = T+ES+EC

            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)

            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]), ('ET', 'T+ES+EC'))
    pdf.savefig()



    #
    # change in SW = PPT - ET - RO - DRAIN
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("$\Delta$SW = PPT-ET-RO-DRAIN")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()

            deltaSW = np.zeros(0)
            for yr in yrs:
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["SW"][-1] -
                          yrs_data[model,treat,exp]["SW"][0])
                deltaSW = np.append(deltaSW, change)

            PPT = df[model,treat,exp].groupby("YEAR").PPT.sum()
            ET = df[model,treat,exp].groupby("YEAR").ET.sum()
            RO = df[model,treat,exp].groupby("YEAR").RO.sum()
            DRAIN = df[model,treat,exp].groupby("YEAR").DRAIN.sum()

            X = deltaSW

            Y = PPT - ET
            if np.all(np.isnan(RO)) == False:
                Y -= RO
            if np.all(np.isnan(DRAIN)) == False:
                Y -= DRAIN

            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)

            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]), ('$\Delta$SW', 'PPT-ET-RO-DRAIN'))
    pdf.savefig()



    #
    # NPP = GPP - Rauto
    #

    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("NPP = GPP - Ra")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()
            NPP = df[model,treat,exp].groupby("YEAR").NPP.sum()
            GPP = df[model,treat,exp].groupby("YEAR").GPP.sum()
            RAUTO = df[model,treat,exp].groupby("YEAR").RAUTO.sum()

            X = NPP
            Y = GPP-RAUTO
            #if model == "CABL":
            #    LabIn = df[model,treat,exp].groupby("YEAR").LabIn.sum()
            #    if np.all(np.isnan(LabIn)) == False:
            #        Y -= LabIn


            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)

            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]), ('NPP', 'GPP-RA'))
    pdf.savefig()




    #
    # NPP = GL + GW + GCR + GR + GREPR + change in TNC + CVOC
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("NPP = GL+GW+GCR+GR+GREPR+$\Delta$TNC+CVOC")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()

            deltaTNC = np.zeros(0)
            for yr in yrs:
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["TNC"][-1] -
                          yrs_data[model,treat,exp]["TNC"][0])
                deltaTNC = np.append(deltaTNC, change)

            NPP = df[model,treat,exp].groupby("YEAR").NPP.sum()
            GL = df[model,treat,exp].groupby("YEAR").GL.sum()
            GW = df[model,treat,exp].groupby("YEAR").GW.sum()
            GCR = df[model,treat,exp].groupby("YEAR").GCR.sum()
            GR = df[model,treat,exp].groupby("YEAR").GR.sum()
            GREPR = df[model,treat,exp].groupby("YEAR").GREPR.sum()
            CVOC = df[model,treat,exp].groupby("YEAR").CVOC.sum()

            X = NPP

            Y = GL + GW
            if np.all(np.isnan(GCR)) == False:
                Y += GCR
            if np.all(np.isnan(GR)) == False:
                Y += GR
            if np.all(np.isnan(deltaTNC)) == False:
                Y += deltaTNC
            if np.all(np.isnan(CVOC)) == False:
                Y += CVOC
            if np.all(np.isnan(GREPR)) == False:
                Y += GREPR

            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)

            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0],
                          ('NPP', 'GL+GW+GCR+GR+GREPR+$\Delta$TNC+CVOC')))

    pdf.savefig()




    #
    # NEP = GPP - Reco
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("NEP = GPP - RECO")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()
            NEP = df[model,treat,exp].groupby("YEAR").NEP.sum()
            GPP = df[model,treat,exp].groupby("YEAR").GPP.sum()
            RECO = df[model,treat,exp].groupby("YEAR").RECO.sum()

            X = NEP
            Y = GPP - RECO


            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)

            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]), ('NEP', 'GPP-RECO'))
    pdf.savefig()




    #
    # RAUTO = RLEAF + RWOOD + RROOT + RGROW
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("RAUTO = RLEAF + RWOOD + RROOT + RGROW")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            RAUTO = df[model,treat,exp].groupby("YEAR").RAUTO.sum()
            RLEAF = df[model,treat,exp].groupby("YEAR").RLEAF.sum()
            RWOOD = df[model,treat,exp].groupby("YEAR").RWOOD.sum()
            RROOT = df[model,treat,exp].groupby("YEAR").RROOT.sum()
            RGROW = df[model,treat,exp].groupby("YEAR").RGROW.sum()

            X = RAUTO
            Y = RLEAF + RWOOD + RROOT + RGROW


            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)

            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)

            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]), ('RAUTO', 'RLEAF+RWOOD+RROOT+RGROW'))
    pdf.savefig()




    #
    # change in CL = GL - LLFALL etc
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("$\Delta$CL = GL - CLLFALL")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()

            deltaCL = np.zeros(0)
            for yr in yrs:

                """
                if model == "LPJX":
                    if yr+1 < yrs.values[-1]:
                        yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                        next_yrs_data = df[df[model,treat,exp]["YEAR"] == yr+1]
                        change = (next_yrs_data[model,treat,exp]["CL"][0] -
                                  yrs_data[model,treat,exp]["CL"][0])
                    else:
                        change = 0.0
                    deltaCL = np.append(deltaCL, change)
                else:
                    yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                    change = (yrs_data[model,treat,exp]["CL"][-1] -
                              yrs_data[model,treat,exp]["CL"][0])
                    deltaCL = np.append(deltaCL, change)
                """
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["CL"][-1] -
                          yrs_data[model,treat,exp]["CL"][0])
                deltaCL = np.append(deltaCL, change)

            GL = df[model,treat,exp].groupby("YEAR").GL.sum()
            CLLFALL = df[model,treat,exp].groupby("YEAR").CLLFALL.sum()

            X = deltaCL
            Y = GL - CLLFALL

            # LPJ
            # The last change is newly reported TNC, as you probably know we
            # don't have TNCs in the model, so in its place I report our C
            # storage. It only affects leaves, so that's the reason that CW
            # balances without it. I would think that it's analogous to the TNC
            # in this sense.
            if model == "LPJX":
                TNC = df[model,treat,exp].groupby("YEAR").TNC.sum()
                Y += TNC

            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)

            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]), ('$\Delta$CL', 'GL-CLLFALL'))
    pdf.savefig()



    #
    # change in CW = GW + GCR - CWIN
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("$\Delta$CW = GW - CWIN")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()

            deltaCW = np.zeros(0)
            for yr in yrs:
                if model == "LPJX":
                    if yr+1 < yrs.values[-1]:
                        yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                        next_yrs_data = df[df[model,treat,exp]["YEAR"] == yr+1]
                        change = (next_yrs_data[model,treat,exp]["CW"][0] -
                                  yrs_data[model,treat,exp]["CW"][0])
                    else:
                        change = 0.0
                    deltaCW = np.append(deltaCW, change)
                else:
                    yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                    change = (yrs_data[model,treat,exp]["CW"][-1] -
                              yrs_data[model,treat,exp]["CW"][0])
                    deltaCW = np.append(deltaCW, change)

            GW = df[model,treat,exp].groupby("YEAR").GW.sum()
            CWIN = df[model,treat,exp].groupby("YEAR").CWIN.sum()

            X = deltaCW
            Y = GW - CWIN

            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)


            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]), ('$\Delta$CW', 'GW-CWIN'))
    pdf.savefig()

    #
    # change in CFR = GR - CFRLIN
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("$\Delta$CFR = GR-CFRLIN")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()

            deltaCFR = np.zeros(0)
            for yr in yrs:
                if model == "LPJX":
                    if yr+1 < yrs.values[-1]:
                        yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                        next_yrs_data = df[df[model,treat,exp]["YEAR"] == yr+1]
                        change = (next_yrs_data[model,treat,exp]["CFR"][0] -
                                  yrs_data[model,treat,exp]["CFR"][0])
                    else:
                        change = 0.0
                    deltaCFR = np.append(deltaCFR, change)
                else:
                    yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                    change = (yrs_data[model,treat,exp]["CFR"][-1] -
                              yrs_data[model,treat,exp]["CFR"][0])
                    deltaCFR = np.append(deltaCFR, change)

            GR = df[model,treat,exp].groupby("YEAR").GR.sum()

            CFRLIN = df[model,treat,exp].groupby("YEAR").CFRLIN.sum()

            X = deltaCFR
            Y = GR - CFRLIN

            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)


            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]), ('$\Delta$CFR', 'GR-CFRLIN'))
    pdf.savefig()


    #
    # change in CCR = GCR - CCRLIN
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("$\Delta$CCR = GCR-CCRLIN")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()

            deltaCCR = np.zeros(0)
            for yr in yrs:
                if model == "LPJX":
                    if yr+1 < yrs.values[-1]:
                        yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                        next_yrs_data = df[df[model,treat,exp]["YEAR"] == yr+1]
                        change = (next_yrs_data[model,treat,exp]["CCR"][0] -
                                  yrs_data[model,treat,exp]["CCR"][0])
                    else:
                        change = 0.0
                    deltaCCR = np.append(deltaCCR, change)
                else:
                    yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                    change = (yrs_data[model,treat,exp]["CCR"][-1] -
                              yrs_data[model,treat,exp]["CCR"][0])
                    deltaCCR = np.append(deltaCCR, change)

            GCR = df[model,treat,exp].groupby("YEAR").GCR.sum()

            CCRLIN = df[model,treat,exp].groupby("YEAR").CCRLIN.sum()

            X = deltaCCR
            Y = GCR - CCRLIN

            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)


            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]), ('$\Delta$CCR', 'GCR-CCRLIN'))
    pdf.savefig()




    #
    # CL = LAI * LMA
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("CL = LAI x LMA")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()
            CL = df[model,treat,exp].groupby("YEAR").CL.mean()
            LAI = df[model,treat,exp].groupby("YEAR").LAI.mean()
            LMA = df[model,treat,exp].groupby("YEAR").LMA.mean()

            X = CL
            Y = LAI*LMA

            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)

            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0],
                            alpha=0.2, edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]), ('CL', 'LAI*LMA'))
    pdf.savefig()




    #
    # NCAN = NCON * CL
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("NCAN = NCON x CL")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()
            NCAN = df[model,treat,exp].groupby("YEAR").NCAN.mean()
            NCON = df[model,treat,exp].groupby("YEAR").NCON.mean()
            CL = df[model,treat,exp].groupby("YEAR").CL.mean()

            X = NCAN
            Y = NCON * CL

            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)


            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]), ('NCAN', 'NCON*CL'))
    pdf.savefig()




    #
    # change in NCAN = NGL - NLITIN - NLRETRANS
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("$\Delta$NCAN = NGL-NLITIN-NLRETRANS")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()

            deltaNCAN  = np.zeros(0)
            for yr in yrs:
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["NCAN"][-1] -
                          yrs_data[model,treat,exp]["NCAN"][0])
                deltaNCAN = np.append(deltaNCAN, change)

            NGL = df[model,treat,exp].groupby("YEAR").NGL.sum()
            NLITIN = df[model,treat,exp].groupby("YEAR").NLITIN.sum()

            NLRETRANS = df[model,treat,exp].groupby("YEAR").NLRETRANS.sum()

            # Inferred retranslocation flux
            #Nretrans = NGL - NLITIN - deltaNCAN

            X = deltaNCAN
            Y = NGL-NLITIN
            if np.all(np.isnan(NLRETRANS)) == False:
                Y -= NLRETRANS
            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)

            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]),
                          ('$\Delta$NCAN', 'NGL-NLITIN-NLRETRANS'))
    pdf.savefig()


    #
    # change in NWOOD = NGW - NWLIN - NWRETRANS
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("$\Delta$NWOOD = NGW-NWLIN-NWRETRANS")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()

            deltaNWOOD  = np.zeros(0)
            for yr in yrs:
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["NWOOD"][-1] -
                          yrs_data[model,treat,exp]["NWOOD"][0])
                deltaNWOOD = np.append(deltaNWOOD, change)

            NGW = df[model,treat,exp].groupby("YEAR").NGW.sum()
            NWLIN = df[model,treat,exp].groupby("YEAR").NWLIN.sum()

            NWRETRANS = df[model,treat,exp].groupby("YEAR").NWRETRANS.sum()

            X = deltaNWOOD
            Y = NGW - NWLIN

            if np.all(np.isnan(NWRETRANS)) == False:
                Y -= NWRETRANS

            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)

            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])

            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]),
                          ('$\Delta$NWOOD', 'NGW-NWLIN-NWRETRANS'))

    pdf.savefig()




    #
    # change in NFR = NGR - NFRLIN - NFRRETRANS
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("$\Delta$NFR = NGR-NFRLIN-NFRRETRANS")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()

            deltaNFR = np.zeros(0)
            for yr in yrs:
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["NFR"][-1] -
                          yrs_data[model,treat,exp]["NFR"][0])
                deltaNFR = np.append(deltaNFR, change)

            NGR = df[model,treat,exp].groupby("YEAR").NGR.sum()
            NFRLIN = df[model,treat,exp].groupby("YEAR").NFRLIN.sum()
            NFRRETRANS = df[model,treat,exp].groupby("YEAR").NFRRETRANS.sum()


            X = deltaNFR
            Y = NGR - NFRLIN
            if np.all(np.isnan(NFRRETRANS)) == False:
                Y -= NFRRETRANS
            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)


            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])

            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]),
                          ('$\Delta$NFR', 'NGR-NFRLIN-NFRRETRANS'))

    pdf.savefig()


    #
    # change in NCR = NGCR - NCRLIN
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("$\Delta$NCR = NGCR-NCRLIN-NCRRETRANS")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()

            deltaNCR = np.zeros(0)
            for yr in yrs:
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["NCR"][-1] -
                          yrs_data[model,treat,exp]["NCR"][0])
                deltaNCR = np.append(deltaNCR, change)

            NGCR = df[model,treat,exp].groupby("YEAR").NGCR.sum()

            NCRLIN = df[model,treat,exp].groupby("YEAR").NCRLIN.sum()
            NCRRETRANS = df[model,treat,exp].groupby("YEAR").NCRRETRANS.sum()


            # Inferred retranslocation flux
            #Nretrans = NGCR - NRLIN - deltaNFR

            X = deltaNCR
            Y = NGCR - NCRLIN
            if np.all(np.isnan(NCRRETRANS)) == False:
                Y -= NCRRETRANS

            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)


            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])

            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]),
                          ('$\Delta$NCR', 'NGCR-NCRLIN-NCRRETRANS'))

    pdf.savefig()



    #
    # NSOIL = NPOOLM + NPOOLO
    #

    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("NSOIL = NPOOLM+NPOOLO")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()
            NSOIL = df[model,treat,exp].groupby("YEAR").NSOIL.sum()
            NPOOLM = df[model,treat,exp].groupby("YEAR").NPOOLM.sum()
            NPOOLO = df[model,treat,exp].groupby("YEAR").NPOOLO.sum()

            X = NSOIL
            Y = NPOOLM
            if np.all(np.isnan(NPOOLO)) == False:
                Y += NPOOLO

            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)

            if model != "CLMP" or model != "CLM4":
                if treat == "AMB":
                    b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                                edgecolor=colour_list[0])
                    b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                                alpha=0.4, edgecolor=colour_list[1])
                else:
                    b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                                edgecolor=colour_list[0])
                    b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                                alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]), ('NSOIL', 'NPOOLM+NPOOLO'))
    pdf.savefig()



    #
    # deltaNCAN+deltaNW+deltaNCR+deltaNFR+deltaNSTOR = NUP - NLITIN-NWLIN-NRLIN
    # Change in plant n content = n uptake - litter loss
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("$\Delta$NCAN+$\Delta$NWOOD+$\Delta$NCR+$\Delta$NFR+$\Delta$NSTOR+$\Delta$NREPR = NUP-NLITIN-NWLIN-NRLIN-NREPRLITIN")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()

            deltaNCAN = np.zeros(0)
            for yr in yrs:
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["NCAN"][-1] -
                          yrs_data[model,treat,exp]["NCAN"][0])
                deltaNCAN = np.append(deltaNCAN, change)

            deltaNWOOD = np.zeros(0)
            for yr in yrs:
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["NWOOD"][-1] -
                          yrs_data[model,treat,exp]["NWOOD"][0])
                deltaNWOOD = np.append(deltaNWOOD, change)

            deltaNCR = np.zeros(0)
            for yr in yrs:
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["NCR"][-1] -
                          yrs_data[model,treat,exp]["NCR"][0])
                deltaNCR = np.append(deltaNCR, change)


            deltaNFR = np.zeros(0)
            for yr in yrs:
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["NFR"][-1] -
                          yrs_data[model,treat,exp]["NFR"][0])
                deltaNFR = np.append(deltaNFR, change)

            deltaNSTOR = np.zeros(0)
            for yr in yrs:
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["NSTOR"][-1] -
                          yrs_data[model,treat,exp]["NSTOR"][0])
                deltaNSTOR = np.append(deltaNSTOR, change)

            if model == "OCNX":
                deltaNREPR = np.zeros(0)
                for yr in yrs:
                    yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                    change = (yrs_data[model,treat,exp]["NREPR"][-1] -
                              yrs_data[model,treat,exp]["NREPR"][0])
                    deltaNREPR = np.append(deltaNREPR, change)

            NUP = df[model,treat,exp].groupby("YEAR").NUP.sum()
            NLITIN = df[model,treat,exp].groupby("YEAR").NLITIN.sum()
            NWLIN = df[model,treat,exp].groupby("YEAR").NWLIN.sum()
            NFRLIN = df[model,treat,exp].groupby("YEAR").NFRLIN.sum()
            NCRLIN = df[model,treat,exp].groupby("YEAR").NCRLIN.sum()
            if model == "OCNX":
                NREPRLITIN = df[model,treat,exp].groupby("YEAR").NREPRLITIN.sum()
            X = deltaNCAN
            if np.all(np.isnan(deltaNWOOD)) == False:
                X += deltaNWOOD
            if np.all(np.isnan(deltaNSTOR)) == False:
                X += deltaNSTOR
            if np.all(np.isnan(deltaNFR)) == False:
                X += deltaNFR
            if np.all(np.isnan(deltaNCR)) == False:
                X += deltaNCR
            if model == "OCNX":
                if np.all(np.isnan(deltaNREPR)) == False:
                    X += deltaNREPR

            Y = NUP - NLITIN - NWLIN
            if np.all(np.isnan(NFRLIN)) == False:
                Y -= NFRLIN
            if np.all(np.isnan(NCRLIN)) == False:
                Y -= NCRLIN
            if model == "OCNX":
                if np.all(np.isnan(NREPRLITIN)) == False:
                    Y -= NREPRLITIN


            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)

            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)

            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]),
                          ('$\Delta$plant N content', 'NUP - litter losses'))


    pdf.savefig()

    """
    #
    # NUP+Nretrans = NGL+NGW+NGR+NGCR + change in NSTORE
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("NUP+Nretrans = NGL+NGW+NGR+NGCR+$\Delta$NSTOR")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()

            deltaNSTOR = np.zeros(0)
            for yr in yrs:
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["NSTOR"][-1] -
                          yrs_data[model,treat,exp]["NSTOR"][0])
                deltaNSTOR = np.append(deltaNSTOR, change)

            deltaNCAN = np.zeros(0)
            for yr in yrs:
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["NCAN"][-1] -
                          yrs_data[model,treat,exp]["NCAN"][0])
                deltaNCAN = np.append(deltaNCAN, change)

            NUP = df[model,treat,exp].groupby("YEAR").NUP.sum()
            NGL = df[model,treat,exp].groupby("YEAR").NGL.sum()
            NGCR  = df[model,treat,exp].groupby("YEAR").NGCR .sum()
            NGR = df[model,treat,exp].groupby("YEAR").NGR.sum()
            NGW  = df[model,treat,exp].groupby("YEAR").NGW.sum()
            NLITIN = df[model,treat,exp].groupby("YEAR").NLITIN.sum()
            Nretrans = NGL - NLITIN - deltaNCAN

            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()

            X = NUP + Nretrans

            Y = NGL + NGW + deltaNSTOR
            if np.all(np.isnan(NGCR)) == False:
                Y += NGCR
            if np.all(np.isnan(NGR)) == False:
                Y += NGR

            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)


            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)

            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]),
                          ('NUP+Nretrans', 'NGL+NGW+NGR+NGCR+$\Delta$NSTOR'))

    pdf.savefig()
    """



    #
    # change in NPOOLM = NMIN + NFIX + NDEP - NVOL - NLEACH - NUP
    #
    ps.fig_setup(two_cols=False, width=10, height=8, margin=.6, TEX=False)
    setup_fig()
    fig = plt.figure()
    fig.suptitle("$\Delta$NPOOLM = NMIN+NFIX+NDEP-NVOL-NLEACH-NUP")
    for i, model in enumerate(model_list):
        ax = fig.add_subplot(3,3,i+1)
        for treat in "AMB", "ELE":
            yrs = df[model,treat,exp].groupby(["YEAR"]).YEAR.mean()

            deltaNPOOLM  = np.zeros(0)
            for yr in yrs:
                yrs_data = df[df[model,treat,exp]["YEAR"] == yr]
                change = (yrs_data[model,treat,exp]["NPOOLM"][-1] -
                          yrs_data[model,treat,exp]["NPOOLM"][0])
                deltaNPOOLM = np.append(deltaNPOOLM, change)

            NMIN = df[model,treat,exp].groupby("YEAR").NMIN.sum()
            NFIX = df[model,treat,exp].groupby("YEAR").NFIX.sum()
            NDEP = df[model,treat,exp].groupby("YEAR").NDEP.sum()
            NVOL = df[model,treat,exp].groupby("YEAR").NVOL.sum()
            NLEACH = df[model,treat,exp].groupby("YEAR").NLEACH.sum()
            NUP = df[model,treat,exp].groupby("YEAR").NUP.sum()

            X = deltaNPOOLM
            Y = NMIN
            if np.all(np.isnan(NFIX)) == False:
                Y += NFIX
            if np.all(np.isnan(NDEP)) == False:
                Y += NDEP
            if np.all(np.isnan(NVOL)) == False:
                Y -= NVOL
            if np.all(np.isnan(NLEACH)) == False:
                Y -= NLEACH
            if np.all(np.isnan(NUP)) == False:
                Y -= NUP

            ind = np.arange(len(X))
            width = 0.2
            ax.set_title(model)

            if treat == "AMB":
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.4,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.4, edgecolor=colour_list[1])
            else:
                b1 = ax.bar(ind, X, width, color=colour_list[0], alpha=0.2,
                            edgecolor=colour_list[0])
                b2 = ax.bar(ind+width, Y, width, color=colour_list[1],
                            alpha=0.2, edgecolor=colour_list[1])

            ax.set_xticks(ind+(width/2.))
            ax.set_xticklabels(["2012", "2018", "2023"])
            ax.set_xticks([0+width, 6+width, 11+width])
            ax.set_xlim(-0.5, 12)


            if i == 0 and treat == "AMB":
                ax.legend((b1[0], b2[0]),
                          ('$\Delta$NPOOLM', 'NMIN+NDEP+NFIX-NVOL-NLEACH-NUP'))
    pdf.savefig()



    pdf.close()

if __name__ == "__main__":

    fdir = "data"
    ofdir = "/Users/mdekauwe/Desktop"
    main(fdir, ofdir, exp="VAR")
