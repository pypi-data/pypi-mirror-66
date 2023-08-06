//
// Created by Mamba on 2020/2/18.
//

#include <Eigen/Eigen>
#include <iostream>

#include "List.h"
#include "Data.h"
#include "Algorithm.h"
#include "Metric.h"

using namespace Eigen;
using namespace std;

List sequential_path(Data &data, Algorithm *algorithm, Metric* metric, Eigen::VectorXi sequence, bool is_warm_start) {
//    std::cout<<"sequence"<<endl;
    int p = data.get_p();
    int n = data.get_n();
    int i;
    int sequence_size = sequence.size();
    Eigen::VectorXi full_mask(n);
    for(i= 0;i<n;i++){
        full_mask(i) = int(i);
    }

//    Eigen::VectorXd aic_sequence(sequence_size);
//    Eigen::VectorXd bic_sequence(sequence_size);
//    Eigen::VectorXd gic_sequence(sequence_size);

    Eigen::VectorXd ic_sequence(sequence_size);
    Eigen::VectorXd loss_sequence(sequence_size);

    Eigen::MatrixXd beta_matrix(p, sequence_size);
    Eigen::VectorXd coef0_sequence(sequence_size);
//    Eigen::VectorXd loss_sequence(sequence_size);

    Eigen::VectorXd beta_init = Eigen::VectorXd::Zero(p);
    double coef0_init = 0.0;

    for (i=0; i < sequence_size; i++) {
//        std::cout<<"sequence_2"<<endl;

        // All data train
        algorithm->update_train_mask(full_mask);
        algorithm->update_sparsity_level(sequence(i));
        algorithm->update_beta_init(beta_init);
        algorithm->update_coef0_init(coef0_init);
        algorithm->fit();

        beta_matrix.col(i) = algorithm->get_beta();
        coef0_sequence(i) = algorithm->get_coef0();
        loss_sequence(i) = metric->train_loss(algorithm, data);

        ic_sequence(i) = metric->ic(algorithm, data);

//        aic_sequence(i) = metric->aic(algorithm, data);
//        bic_sequence(i) = metric->bic(algorithm, data);
//        gic_sequence(i) = metric->gic(algorithm, data);
//        loss_sequence(i) = algorithm->get_loss();

        if(is_warm_start) {
            beta_init = algorithm->get_beta();
            coef0_init = algorithm->get_coef0();
        };
    }

    if(data.is_normal){
        if(algorithm->model_type == 1)
        {
            for(i=0;i<sequence_size;i++){
                beta_matrix.col(i) = sqrt(double(n))*beta_matrix.col(i).cwiseQuotient(data.x_norm);
                coef0_sequence(i) = data.y_mean - beta_matrix.col(i).dot(data.x_mean);
            }
        }
        else if(algorithm->model_type == 2)
        {
            for(i=0;i<sequence_size;i++){
                beta_matrix.col(i) = sqrt(double(n))*beta_matrix.col(i).cwiseQuotient(data.x_norm);
                coef0_sequence(i) = coef0_sequence(i) - beta_matrix.col(i).dot(data.x_mean);
            }
        }
    }


//    //    all sequence output
//    #ifdef R_BUILD
//        return List::create(Named("beta")=beta_matrix, Named("coef0")=coef0_sequence, Named("loss")=loss_sequence, Named("A")=algorithm->get_A_out(), Named("l")=sequence_size);
//    #else
//        List mylist;
//        mylist.add("beta", beta_matrix);
//        mylist.add("coef0", coef0_sequence);
//        mylist.add("ic", ic_sequence);
//        mylist.add("A", algorithm->get_A_out());
//        mylist.add("l", sequence_size);
//        return mylist;
//    #endif

    //  find min_loss parameter
    double min_loss = ic_sequence(0);
    int min_loss_index = 0;
    for(i=1;i<sequence_size;i++){
        if(ic_sequence(i) < min_loss){
            min_loss = ic_sequence(i);
            min_loss_index = i;
        }
    }

    #ifdef R_BUILD
        return List::create(Named("beta")=beta_matrix.col(min_loss_index).eval(), Named("coef0")=coef0_sequence(min_loss_index), Named("ic")=ic_sequence(min_loss_index));
    #else
        List mylist;
        mylist.add("beta", beta_matrix.col(min_loss_index).eval());
        mylist.add("coef0", coef0_sequence(min_loss_index));
        mylist.add("train_loss", loss_sequence(min_loss_index));
        mylist.add("ic", ic_sequence(min_loss_index));
        return mylist;
    #endif
}

List gs_path(Data &data, Algorithm *algorithm, Metric* metric, int s_min, int s_max, int K_max, double epsilon, bool is_warm_start) {
//    std::cout<<"gs"<<endl;
    int p = data.get_p();
    int n = data.get_n();
    int i;
    Eigen::VectorXi full_mask(n);
    for(i= 0;i<n;i++){
        full_mask(i) = int(i);
    }

//    Eigen::VectorXd aic_sequence(sequence_size);
//    Eigen::VectorXd bic_sequence(sequence_size);
//    Eigen::VectorXd gic_sequence(sequence_size);
//
//    Eigen::MatrixXd beta_matrix(p, 2);
//    Eigen::VectorXd coef0_sequence(2);
//    Eigen::VectorXd loss_sequence(2);
//    Eigen::VectorXd ic_sequence(2);

    Eigen::VectorXd beta_init = Eigen::VectorXd::Zero(p);
    double coef0_init = 0.0;

    int Tmin = s_min;
    int Tmax = s_max;
    int T1;
    int T2;
    double icT1;
    double icT2;

    while(Tmax-Tmin >2)
    {
        T1 = floor(0.618 * Tmin + 0.382 * Tmax);
        T2 = ceil(0.382 * Tmin + 0.618 * Tmax);
        algorithm->update_train_mask(full_mask);
        algorithm->update_sparsity_level(T1);
        algorithm->update_beta_init(beta_init);
        algorithm->update_coef0_init(coef0_init);
        algorithm->fit();
        icT1 = metric->ic(algorithm, data);

        if (is_warm_start) {
        beta_init = algorithm->get_beta();
        coef0_init = algorithm->get_coef0();
        }

        algorithm->update_train_mask(full_mask);
        algorithm->update_sparsity_level(T2);
        algorithm->update_beta_init(beta_init);
        algorithm->update_coef0_init(coef0_init);
        algorithm->fit();
        icT2 = metric->ic(algorithm, data);

        if (is_warm_start) {
        beta_init = algorithm->get_beta();
        coef0_init = algorithm->get_coef0();
        }

        if(icT1<icT2) Tmax=T2;
        else Tmin=T1;
    }

    Eigen::VectorXd best_beta;
    double best_coef0;
    double best_train_loss;
    double best_ic;
    if(Tmax == Tmin)
    {
        algorithm->update_train_mask(full_mask);
        algorithm->update_sparsity_level(Tmin);
        algorithm->update_beta_init(beta_init);
        algorithm->update_coef0_init(coef0_init);
        algorithm->fit();
        best_beta = algorithm->get_beta();
        best_coef0 = algorithm->get_coef0();
        best_train_loss = metric->train_loss(algorithm, data);
        best_ic = metric->ic(algorithm, data);
    }
    else if(Tmax == Tmin + 1)
    {
        algorithm->update_train_mask(full_mask);
        algorithm->update_sparsity_level(Tmin);
        algorithm->update_beta_init(beta_init);
        algorithm->update_coef0_init(coef0_init);
        algorithm->fit();
        best_beta = algorithm->get_beta();
        best_coef0 = algorithm->get_coef0();
        best_train_loss = metric->train_loss(algorithm, data);
        best_ic = metric->ic(algorithm, data);

        algorithm->update_train_mask(full_mask);
        algorithm->update_sparsity_level(Tmax);
        algorithm->update_beta_init(beta_init);
        algorithm->update_coef0_init(coef0_init);
        algorithm->fit();

        if(metric->ic(algorithm, data) < best_ic)
        {
            best_beta = algorithm->get_beta();
            best_coef0 = algorithm->get_coef0();
            best_train_loss = metric->train_loss(algorithm, data);
            best_ic = metric->ic(algorithm, data);
        }


    }
    else if(Tmax == Tmin + 2)
    {
        algorithm->update_train_mask(full_mask);
        algorithm->update_sparsity_level(Tmin);
        algorithm->update_beta_init(beta_init);
        algorithm->update_coef0_init(coef0_init);
        algorithm->fit();
        best_beta = algorithm->get_beta();
        best_coef0 = algorithm->get_coef0();
        best_train_loss = metric->train_loss(algorithm, data);
        best_ic = metric->ic(algorithm, data);
        for(int t=1;t<=2;t++)
        {
            algorithm->update_train_mask(full_mask);
            algorithm->update_sparsity_level(Tmin + t);
            algorithm->update_beta_init(beta_init);
            algorithm->update_coef0_init(coef0_init);
            algorithm->fit();
            if(metric->ic(algorithm, data) < best_ic)
            {
                best_beta = algorithm->get_beta();
                best_coef0 = algorithm->get_coef0();
                best_train_loss = metric->train_loss(algorithm, data);
                best_ic = metric->ic(algorithm, data);
            }
        }
    }
    if(data.is_normal){
        if(algorithm->model_type == 1)
        {
            best_beta = sqrt(double(n))*best_beta.cwiseQuotient(data.x_norm);
            best_coef0 = data.y_mean - best_beta.dot(data.x_mean);
        }
        else if(algorithm->model_type == 2)
        {
            best_beta = sqrt(double(n))*best_beta.cwiseQuotient(data.x_norm);
            best_coef0 = best_coef0 - best_beta.dot(data.x_mean);
        }
    }

    #ifdef R_BUILD
        return List::create(Named("beta")=beta_matrix.col(min_loss_index).eval(), Named("coef0")=coef0_sequence(min_loss_index), Named("ic")=ic_sequence(min_loss_index));
    #else
        List mylist;
        mylist.add("beta", best_beta);
        mylist.add("coef0", best_coef0);
        mylist.add("train_loss", best_train_loss);
        mylist.add("ic", best_ic);
        return mylist;
    #endif


//    int k;
//    algorithm->update_train_mask(full_mask);
//    algorithm->update_sparsity_level(sL);
//    algorithm->update_beta_init(beta_init);
//    algorithm->update_coef0_init(coef0_init);
//    algorithm->fit();
//
//    beta_matrix.col(0) = algorithm->get_beta();
//    coef0_sequence(0) = algorithm->get_coef0();
//    loss_sequence(0) = metric->train_loss(algorithm, data);
//
//    ic_sequence(0) = metric->ic(algorithm, data);
//
////    algorithm->update_sparsity_level(sL);
////    algorithm->update_beta_init(beta_init);
////    algorithm->update_coef0_init(coef0_init);
////    algorithm->run();
////
////    aic_sequence(0) = metric->aic(algorithm, data);
////    bic_sequence(0) = metric->bic(algorithm, data);
////    gic_sequence(0) = metric->gic(algorithm, data);
////    beta_matrix.col(0) = algorithm->get_beta();
////    coef0_sequence(0) = algorithm->get_coef0();
////    loss_sequence(0) = algorithm->get_loss();
//    T_sequence(0) = sL;
//
//    if (is_warm_start) {
//        beta_init = algorithm->get_beta();
//        coef0_init = algorithm->get_coef0();
//    }
//
//    algorithm->update_train_mask(full_mask);
//    algorithm->update_sparsity_level(sR);
//    algorithm->update_beta_init(beta_init);
//    algorithm->update_coef0_init(coef0_init);
//    algorithm->fit();
//
//    beta_matrix.col(1) = algorithm->get_beta();
//    coef0_sequence(1) = algorithm->get_coef0();
//    loss_sequence(1) = metric->train_loss(algorithm, data);
//
//    ic_sequence(1) = metric->ic(algorithm, data);
//    T_sequence(1) = sR;
//
//    if (is_warm_start) {
//        beta_init = algorithm->get_beta();
//        coef0_init = algorithm->get_coef0();
//    }
//
//    lossL = ic_sequence(0);
//    lossL1 = lossL;
//    lossR = ic_sequence(1);
//    nullloss = data.get_nullloss();
//
//    for(k=2;k<=K_max+1;k++){
//        sM1 = round(0.382*sR + 0.618 * sL));
//        algorithm->update_train_mask(full_mask);
//        algorithm->update_sparsity_level(sM);
//        algorithm->update_beta_init(beta_init);
//        algorithm->update_coef0_init(coef0_init);
//        algorithm->fit();
//
//        beta_matrix.col(k) = algorithm->get_beta();
//        coef0_sequence(k) = algorithm->get_coef0();
//        loss_sequence(k) = metric->train_loss(algorithm, data);
//
//        ic_sequence(k) = metric->ic(algorithm, data);
//
//        T_sequence(k) = sM1;
//
//        if (is_warm_start) {
//            beta_init = algorithm->get_beta();
//            coef0_init = algorithm->get_coef0();
//        }
//
//        lossM1 = ic_sequence(k);
//
//        if((abs(lossL - lossM)/abs(nullloss*(sM - sL)) > epsilon) && (abs(lossR - lossM)/abs(nullloss*(sM - sR)) < epsilon)) {
//            sR = sM;
//            lossR = lossM;
//        } else if((abs(lossL - lossM)/abs(nullloss*(sM - sL)) > epsilon) && (abs(lossR - lossM)/abs(nullloss*(sM - sR)) > epsilon)) {
//            sL = sM;
//            lossL = lossM;
//        } else {
//            sR = sM;
//            lossR = lossM;
//            sL = s_min;
//            lossL = lossL1;
//        }
//        if(sR - sL == 1) break;
////        if(warm_start) {
////            beta_0ML = beta_0M;
////            beta_0MR = beta_0M;
////        } else {
////            beta_0ML = beta0;
////            beta_0MR = beta0;
////        }
//
//        algorithm->update_train_mask(full_mask);
//        algorithm->update_sparsity_level(sM-1);
//        algorithm->update_beta_init(beta_init);
//        algorithm->update_coef0_init(coef0_init);
//        algorithm->fit();
//
////        beta_matrix.col(0) = algorithm->get_beta();
////        coef0_sequence(0) = algorithm->get_coef0();
//        lossML  = metric->train_loss(algorithm, data);
//
////        algorithm->update_sparsity_level(sM - 1);
////        algorithm->update_beta_init(beta_init);
////        algorithm->update_coef0_init(coef0_init);
////        algorithm->run();
////        lossML = algorithm->get_loss();
//
//        algorithm->update_train_mask(full_mask);
//        algorithm->update_sparsity_level(sM);
//        algorithm->update_beta_init(beta_init);
//        algorithm->update_coef0_init(coef0_init);
//        algorithm->fit();
//
////        beta_matrix.col(0) = algorithm->get_beta();
////        coef0_sequence(0) = algorithm->get_coef0();
//        lossMR = metric->train_loss(algorithm, data);
//
////        algorithm->update_sparsity_level(sM + 1);
////        algorithm->update_beta_init(beta_init);
////        algorithm->update_coef0_init(coef0_init);
////        algorithm->run();
////        lossMR = algorithm->get_loss();
//
//        if((abs(lossML - lossM)/nullloss > epsilon) && (2*abs(lossMR - lossM)/nullloss < epsilon)) break;
//    }
//    if(k>K_max+1) k = K_max+1;
////    Eigen::VectorXd ic_sequence(sequence_size);
//
////    for(int i=0;i<=k;i++){
////        if(metric->ic_type == 1)
////            ic_sequence(i) = double(n)*log(loss_sequence(i))+2.0*T_sequence(i);
////        else if(metric->ic_type == 2)
////            ic_sequence(i) = double(n)*log(loss_sequence(i))+log(double(n))*T_sequence(i);
////        else
////            ic_sequence(i) = double(n)*log(loss_sequence(i))+log(double(p))*log(log(double(n)))*T_sequence(i);
////    }
//
//    if(data.is_normal){
//        if(algorithm->model_type == 1)
//        {
//            for(i=0;i<k;i++){
//                beta_matrix.col(i) = sqrt(double(n))*beta_matrix.col(i).cwiseQuotient(data.x_norm);
//                coef0_sequence(i) = data.y_mean - beta_matrix.col(i).dot(data.x_mean);
//            }
//        }
//        else if(algorithm->model_type == 2)
//        {
//            for(i=0;i<k;i++){
//                beta_matrix.col(i) = sqrt(double(n))*beta_matrix.col(i).cwiseQuotient(data.x_norm);
//                coef0_sequence(i) = coef0_sequence(i) - beta_matrix.col(i).dot(data.x_mean);
//            }
//        }
//    }
//
//    //  all sequence output
//    #ifdef R_BUILD
//    return List::create(Named("beta")=beta_matrix.leftCols(k+1), Named("coef0")=coef0_sequence.head(k+1)), Named("ic")=ic_sequence, Named("A")=algorithm->get_A_out(), Named("l")=k);
//    #else
//    List mylist;
//    mylist.add("beta", beta_matrix.leftCols(k+1).eval());
//    mylist.add("coef0", coef0_sequence.head(k+1).eval());
//    mylist.add("s_list", T_sequence.head(k+1).eval());
//    mylist.add("ic", ic_sequence.head(k+1).eval());
//    mylist.add("A", algorithm->get_A_out());
//    mylist.add("l", k);
//    return mylist;
//    #endif

//    double min_loss = ic_sequence(0);
//    int min_loss_index = 0;
//    for(i=1;i<=k;i++){
//        if(ic_sequence(i) < min_loss){
//            min_loss = ic_sequence(i);
//            min_loss_index = i;
//        }
//    }
//
//    #ifdef R_BUILD
//        return List::create(Named("beta")=beta_matrix.col(min_loss_index).eval(), Named("coef0")=coef0_sequence(min_loss_index), Named("ic")=ic_sequence(min_loss_index));
//    #else
//        List mylist;
//        mylist.add("beta", beta_matrix.col(min_loss_index).eval());
//        mylist.add("coef0", coef0_sequence(min_loss_index));
//        mylist.add("train_loss", loss_sequence(min_loss_index));
//        mylist.add("ic", ic_sequence(min_loss_index));
//        return mylist;
//    #endif
}