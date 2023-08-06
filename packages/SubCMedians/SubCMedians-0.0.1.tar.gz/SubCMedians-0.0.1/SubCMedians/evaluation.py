from scipy.optimize import linear_sum_assignment
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
epsilon = 1e-5

def plot_projection(centers,X,y_pred,x=0,y=1):
    X_full = pd.DataFrame(X)
    X_full["cluster"] =  ["clus. "+str(v) for v in y_pred]
    X_full["cluster"] = X_full["cluster"].astype('category')
    sns.scatterplot(x=x, y=y, hue='cluster', marker=".", data=X_full)
    sns.scatterplot(x=x, y=y, marker="o", data=pd.DataFrame(centers))
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()

def plot_evolution(variables,name):
    for k in variables:
        plt.plot(variables[k],label=k)
    plt.xlabel("Iterations",fontsize=20)
    plt.ylabel(name,fontsize=20)
    plt.legend()
    plt.tight_layout()
    plt.show()

def cross_tab(y_pred,y_true):
    res = pd.DataFrame([y_true,y_pred]).T
    return(pd.crosstab(y_true,y_pred))

def plot_cross_tab(y_pred,y_true):
    ct = cross_tab(y_pred,y_true)
    sns.heatmap(ct,annot=True)
    b, t = plt.ylim()
    b += 0.5
    t -= 0.5 
    plt.ylim(b, t)
    plt.tight_layout()

def _mapped(crosstab):
    mapped_clusters = (crosstab.T * 1. / crosstab.sum(1)).T
    return mapped_clusters == mapped_clusters.max(0)

def entropy_score(crosstab):
    found_clusters_effective = crosstab.sum(0)
    p_h_in_c = crosstab * 1. / (found_clusters_effective + epsilon)
    log_p_h_in_c = np.log(p_h_in_c+epsilon)
    pre_ec = -1. * p_h_in_c * log_p_h_in_c
    pre_ec = pre_ec.fillna(0)
    ec = pre_ec.sum(0)
    num = (ec * found_clusters_effective).sum()
    denum = found_clusters_effective.sum() * np.log(len(crosstab.index))
    return 1. - num * 1. / denum

def accurracy_score(crosstab):
    best_matching_y_true = crosstab == crosstab.max(0)
    best_matching_y_true_weight = 1./best_matching_y_true.sum(0)
    correctly_predicted_objects = crosstab * best_matching_y_true * best_matching_y_true_weight
    return correctly_predicted_objects.sum().sum() * 1. / crosstab.sum().sum()

def ce_score(crosstab):
    cost = crosstab.values
    row_ind, col_ind = linear_sum_assignment(-cost)
    best_assignment = cost[row_ind, col_ind].sum()
    return(best_assignment / (cost.sum().sum() + epsilon))

def recall_score(crosstab):
    mapped_clusters = _mapped(crosstab)
    mapped_clusters = (crosstab.T * 1. / crosstab.sum(1)).T
    num = mapped_clusters * crosstab
    num = num.sum(1)
    denum = crosstab.sum(1)
    return num * 1. / (denum + epsilon)

def precision_score(crosstab):
    mapped_clusters = _mapped(crosstab)
    num = mapped_clusters * crosstab
    num = num.sum(1)
    denum = mapped_clusters * crosstab.sum(0)
    denum = denum.sum(1)
    return num * 1. / (denum + epsilon)

def f1_score(crosstab):
    recall = recall_score(crosstab)
    precision = precision_score(crosstab)
    denum = recall + precision
    num = 2 * recall * precision
    return(num/denum)

def evaluate(y_true,y_pred):
    crosstab = cross_tab(y_true,y_pred).T
    entropy = entropy_score(crosstab)
    accuracy = accurracy_score(crosstab)
    ce = ce_score(crosstab)
    recall = recall_score(crosstab)
    precision = precision_score(crosstab)
    f1 = f1_score(crosstab)
    results={"accuracy":accuracy,
             "f1":f1.mean(),
             "precision":precision.mean(),
             "recall":recall.mean(),
             "entropy":entropy,
             "ce":ce}
    return(results)
