# Met2Img (deepmg): Metagenomic data To Images using Deep learning

Met2Img (deepmg) is a computational framework for metagenomic analysis using Deep learning and classic learning algorithms:
(converted to **_python3_** since April, 26th, 2019 (since version 1.0.0))
* Supports to **_VISUALIZE_** data into 2D images, **_TRAIN_** data shaped 1D or 2D with many different algorithms and **_PREDICT_** new data with a pretrained network.
* Provides a variety of binnings: SPB, QTF, MMS,...
* Supports numerous methods for visualizing data including **Fill-up**, t-Distributed Stochastic Neighbor Embedding (t-SNE), Linear Discriminant Analysis (LDA), Isomap, Principal Component Analysis (PCA), Random Projection (RD_Pro), Multidimensional Scaling (MDS), Spectral Embeddings (SE), Non-Negative Matrix Factorization (NMF), Locally Linear Embedding (LLE).
* Provides a vast of classifiers (Convolutional Neural Networks, Linear Regression, Random Forests (RFs), Support Vector Machines (SVMs), K-nearest neighbors, Gradient Boosting, k-Nearest Neighbors... also can be loaded from a pretrained network and be able to extend easily) for 1D and 2D data.
* Comprises cross-validation analysis with internal validation and external validation (optional) as well as holdout validation.
* Supports to reduce dimension (for very-dimensional data) before visualizing with PCA, RD_Pro
* Flexibility for testing models with a large range of parameters provided.
* Supports various datatypes, such as abundance and read counts with different levels of OTUs such as species, genus...
* Evaluates models with various metrics: Accuracy (ACC), Area Under Curve (AUC), Matthews Correlation Coefficient (MCC), f1-score, confusion matrix,...
* 25 available datasets with > 5000 samples for test (download from [Met2img,deepmg]( https://git.integromics.fr/published/deepmg))
* The package is now available to install by pip command, supporting **_MacOS, Linux, Windows_** (since v. 1.0.21)
* **_Met2Bin_** is an extended version to generate 1D representations.

# References:

Please cite Met2Img (deepmg) in your publications if it helped your research. Thank you very much!
<!-- 
```
@article{deepmg_lda,
	author = {Thanh Hai Nguyen and Edi Prifti and Nataliya Sokolovska and Jean-Daniel Zucker},
	title = {Disease Prediction using Synthetic Image Representations of Metagenomic data and Convolutional Neural Networks},
	pages = {231-236},
	Journal = {The 13th IEEE-RIVF International Conference on Computing and Communication Technologies 2019},	
	year = {2019},
	month = {March},
	publisher = {IEEE Xplore}
}
```
-->
```
@InProceedings{deepmg,
    author = {Thanh Hai Nguyen and
               Edi Prifti and
               Nataliya Sokolovska and
               Jean{-}Daniel Zucker},
    title = {Disease Prediction using Synthetic Image Representations of Metagenomic data and Convolutional Neural Networks},
    booktitle = {Proceedings of The 13th IEEE-RIVF International Conference on Computing and Communication Technologies},
    month = March,
    year = 2019,
    publisher = {IEEE},
    pages = {231-236},
}
```

# Getting Started

## Prerequisites

<!--
* These packages should be installed before using Met2Img (updated to 21/02/2018):

```
tensorflow	1.5.0
sklearn	0.19.1
keras	2.1.3
numpy	1.14.0
matplotlib	2.1.2
```
-->
* Please install if you do not have:
python3.6

```
pip install numpy
pip install matplotlib
pip install ConfigParser
pip install pandas
pip install sklearn
pip install tensorflow==1.14
pip install keras
pip install keras_sequential_ascii
pip install minisom
pip install pillow
```

* In order to use the packages for explanation of the network trained, please download and install:

[Grad-Cam, Saliency] (https://github.com/jacobgil/keras-grad-cam)

[LIME] (https://github.com/marcotcr/lime/tree/master/doc/notebooks)

## Install or Download the package Met2Img

In order to install the package

```
pip install deepmg
```

In order to download the package
```
git clone https://git.integromics.fr/published/deepmg
```

# Running Experiments
## How to use Met2Img

* **Input**: 
  - mandatory: csv files containing data (\*_x.csv) and labels (\*_y.csv) 
  - optional: if use external validation set: data (\*z_x.csv) and labels (\*z_y.csv)) put in [data](data/) changable with parameters *--orginal_data_folder*). 
  
  For examples, cirphy_x.csv and cirphy_y.csv for Cirrhosis dataset in [MetAML] (https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004977) ONLY for internal validations; and ibdtrainHS_UCr_x.csv ibdtrainHS_UCr_y.csv ibdtrainHS_UCrz_x.csv ibdtrainHS_UCrz_y.csv for a dataset in [Sokol's] (https://www.ncbi.nlm.nih.gov/pubmed/26843508) datasets containing external validation set.

* **Output**:

  - *images*: Met2Img will generate images and store them in [images/*name_dataset_parameters_to_generate_image*/] (images/) (changable with parameters **--parent_folder_img**)

  - *results*: performance/training/testing information of each fold and summary results put in    [results/*name_dataset_parameters_to_generate_image*/] (results/) (changable with parameters **--parent_folder_results**), includes more than 5 files: 
      - \*file_sum.txt: parameters used to run, performance at each fold. The last rows show training/testing performance in ACC, AUC, execution time, and other metrics of the experiment. When the experiment finishes, a suffix "_ok" (changable with parameters **--suff_fini**) appended to the name of file marking that the experiment finishes.

      - \*file_eachfold.txt (if **--save_folds=y**): results of each fold with accuracy, auc, mcc, loss of training and testing.
      
      - \*file_mean_acc.txt (if **--save_avg_run=y**): if the experiment includes *n* runs repeated independently, so the file includes average performance on *k*-folds of each run measured by **accuracy** and time execution at training/testing of beginning, training/testing when finished.

      - \*file_mean_auc.txt (if **--save_avg_run=y**): if the experiment includes *n* runs repeated independently, so the file includes average performance on *k*-folds of each run measured by **AUC**  at training/testing of beginning, training/testing when finished.

      - If **--save_para=y**: configuration file to repeat the experiment
  
      - If use **--save_w=y** (save weights of trained networks) and/or **--save_entire_w=y**, **--save_d=y**, then 2 folders will be created:
    
          - results/*name_dataset_parameters_to_generate_image*/models/: includes \*weightmodel\*.json contains structure of the model \*weightmodel\*.h5 stores weights.

          - results/*name_dataset_parameters_to_generate_image*/details/\*weight_\*.txt: contains accuracy and loss of training and testing every epochs **--save_d=y**. If **--save_rf=y**, then we will have important scores generated from RFs for each run.
        
      

* Get help to see parameters in the package: 

```
Usage: python -m deepmg [options]

Options:
  -h, --help            show this help message and exit
  -a TYPE_RUN, --type_run=TYPE_RUN
                        Select a type of processing, visual (vis)
                        transformation of the data, learning (learn) a model,
                        testing it in another dataset, or predicting (predict)
                        new data, or creating config file (config)
  --config_file=CONFIG_FILE
                        Specify the path of the config file if reading
                        parameters from files
  --seed_value_begin=SEED_VALUE_BEGIN
                         set the beginning seed for different runs (default:1)
  --search_already=SEARCH_ALREADY
                        if y: search existed experiments before running-->if
                        existed, stopping the experiment (default:y)
  --cudaid=CUDAID       id of the gpu card to use when multiple exist in the
                        server (if <=-3: use CPU, -2: use cpu if no available
                        gpu, -1: use all gpu, >=0: id of gpu), (default:-3)
  --gpu_memory_fraction=GPU_MEMORY_FRACTION
                        gpu_memory_fraction for running by cuda
                        (0:auto_increase based on requirement)
  --rd_pr_seed=RD_PR_SEED
                         seed for random projection (default:None)
  --debug=DEBUG         show DEBUG if >0 (default:0)
  --check=CHECK         check whether package can work properly or not (if
                        there is any error in installation)
  --grid_coef_time=GRID_COEF_TIME
                        choose the best coef from #coef default for tuning
                        coeficiency (default:5)
  --cv_coef_time=CV_COEF_TIME
                        k-cross validation for each coef for tuning
                        coeficiency (default:4)
  --coef_ini=COEF_INI   initilized coefficient for tuning coeficiency
                        (default:255)
  --metric_selection=METRIC_SELECTION
                        roc_auc/accuracy/neg_log_loss/grid_search_mmc for
                        tuning coeficiency (default:roc_auc)
  --parent_folder_img=PARENT_FOLDER_IMG
                        name of parent folder containing images
                        (default:images)
  -r ORIGINAL_DATA_FOLDER, --original_data_folder=ORIGINAL_DATA_FOLDER
                        parent folder containing data (default:data)
  -i DATA_NAME, --data_name=DATA_NAME
                        name of dataset (default:wt2phy)
  --parent_folder_results=PARENT_FOLDER_RESULTS
                        parent folder containing results (default:results)
  --save_avg_run=SAVE_AVG_RUN
                        save avg performance of each run
  --save_labels=SAVE_LABELS
                        save labels of each fold
  --save_d=SAVE_D       saving details of learning (details of each epoch -->
                        may consume more storage
  --save_w=SAVE_W       save weight mode, default:n, this might consume much
                        storage
  --suff_fini=SUFF_FINI
                        append suffix when finishing (default:ok), used to
                        mark finished experiment
  --save_rf=SAVE_RF     save important features and scores for Random Forests
  --save_para=SAVE_PARA
                        save parameters to config files
  --path_config_w=PATH_CONFIG_W
                        path of config to save, if empty, save to the same
                        folder of the results
  --ext_data=EXT_DATA   external data with a pattern name (eg. wt2dphy),
                        default: empty
  --save_entire_w=SAVE_ENTIRE_W
                        save weight of model on whole datasets (default:n)
  --save_folds=SAVE_FOLDS
                        save results of each fold
  --sound_fini=SOUND_FINI
                        play sound when finished (work on MacOS, default: n)
  -k N_FOLDS, --n_folds=N_FOLDS
                        number of k folds (default:10), if k == 1, training on
                        whole *_x.csv, and testing on *z_x.csv
  --test_ext=TEST_EXT   if==y, using external validation sets (default:n)
  --run_time=RUN_TIME   give the #runs (default:1)
  --whole_run_time=WHOLE_RUN_TIME
                        give the #runs (default:1)
  --preprocess_img=PREPROCESS_IMG
                        support resnet50/vgg16/vgg19, none: no use
                        (default:none)
  --pretrained_w_path=PRETRAINED_W_PATH
                        path to a pretrained model, used for testing,
                        predicting or continue to train a data
  --test_size=TEST_SIZE
                        test size in holdout validation, if != 0 or != 1, then
                        do cross validation
  -f NUMFILTERS, --numfilters=NUMFILTERS
                        #filters/neurons for each cnn/neural layer
  -n NUMLAYERCNN_PER_MAXPOOL, --numlayercnn_per_maxpool=NUMLAYERCNN_PER_MAXPOOL
                        #cnnlayer before each max pooling (default:1)
  --nummaxpool=NUMMAXPOOL
                        #maxpooling_layer (default:1)
  --dropout_cnn=DROPOUT_CNN
                         dropout rate for CNN layer(s) (default:0)
  -d DROPOUT_FC, --dropout_fc=DROPOUT_FC
                        dropout rate for FC layer(s) (default:0)
  --padding=PADDING     y if use pad, others: does not use (default:n)
  --filtersize=FILTERSIZE
                        the filter size (default:3)
  --poolsize=POOLSIZE   the pooling size (default:2)
  --model=MODEL         model name for learning vgglike/model_lstm/resnet50/rf
                        _model/dtc_model/gbc_model/svm_model/knn_model/none/)
  -c NUM_CLASSES, --num_classes=NUM_CLASSES
                        #output of the network (default:1)
  -e EPOCH, --epoch=EPOCH
                        the epoch used for training (default:500)
  --learning_rate=LEARNING_RATE
                         learning rate, if -1 use default value of the
                        optimizer (default:-1)
  --batch_size=BATCH_SIZE
                        batch size (default:16)
  --learning_rate_decay=LEARNING_RATE_DECAY
                        learning rate decay (default:0)
  --momentum=MOMENTUM   momentum (default:0)
  -o OPTIMIZER, --optimizer=OPTIMIZER
                        support sgd/adam/Adamax/RMSprop/Adagrad/Adadelta/Nadam
                        (default:adam)
  -l LOSS_FUNC, --loss_func=LOSS_FUNC
                        support binary_crossentropy/mae/squared_hinge/categori
                        cal_crossentropy  (default:binary_crossentropy)
  -q E_STOP, --e_stop=E_STOP
                        #epochs with no improvement after which training will
                        be stopped (default:5)
  --e_stop_consec=E_STOP_CONSEC
                        option to choose consective (self defined: consec)
                        consec or  norma, default:consec
  --svm_c=SVM_C         Penalty parameter C of the error term for SVM
  --svm_kernel=SVM_KERNEL
                        the kernel type used in the algorithm (linear, poly,
                        rbf, sigmoid, precomputed) (default:linear)
  --rf_n_estimators=RF_N_ESTIMATORS
                        The number of trees in the forest (default:500)
  --rf_max_features=RF_MAX_FEATURES
                        The number of max features in the forest (default:-2:
                        auto (sqrt), -1: all)
  --rf_max_depth=RF_MAX_DEPTH
                        The number of deep tree (default:-1: None)
  --knn_n_neighbors=KNN_N_NEIGHBORS
                        The Number of neighbors to use (default:5) in
                        KNeighborsClassifier
  -z COEFF, --coeff=COEFF
                        coeffiency (divided) for input (should use 255 for
                        images) (default:1)
  --orderf_fill=ORDERF_FILL
                        shuffle order of feature (not for manifolds learning):
                        if none, use original order of data, if high: higher
                        composition will be in the top  (default:none)
  --new_dim=NEW_DIM     new dimension after reduction (default:676)
  --path_vis_learn=PATH_VIS_LEARN
                        read config for generating images (for qtf/mms combine
                        fills/manifolds)
  --path_data_vis_learn=PATH_DATA_VIS_LEARN
                        path to read learned data for visualizing (for qtf/mms
                        combine fills/manifolds)
  --del0=DEL0           if y, delete features have nothing, default: n
  --lr_visual=LR_VISUAL
                        learning rate for generating visualizations
                        (default:100.0)
  --label_visual=LABEL_VISUAL
                        use label when using t-SNE:'': does not use
  --iter_visual=ITER_VISUAL
                        #iteration for run algorithm for visualization; for
                        tsne, it should be at least 250, but  do not set so
                        high (default:300)
  --ini_visual=INI_VISUAL
                        ini for visualization algorithm (default:pca)
  --method_lle=METHOD_LLE
                        method for lle embedding:
                        standard/ltsa/hessian/modified (default:standard)
  --eigen_solver=EIGEN_SOLVER
                        method for others (except for tsne) (default:auto)
  --cmap_vmin=CMAP_VMIN
                         vmin for cmap (default:0)
  --cmap_vmax=CMAP_VMAX
                        vmax for cmap (default:1)
  --scale_mode=SCALE_MODE
                        scaler mode for input (default: Null)
  --n_quantile=N_QUANTILE
                        n_quantile in quantiletransformer (default:1000)
  --min_scale=MIN_SCALE
                        minimum value for scaling (only for minmaxscaler)
  --max_scale=MAX_SCALE
                        maximum value for scaling (only for minmaxscaler)
  --min_v=MIN_V         limit min for Equal Width Binning (default:0)
  --max_v=MAX_V         limit max for Equal Width Binning (default:1), affect
                        for eqw ONLY
  --num_bin=NUM_BIN     the number of bins (default:10)
  --auto_v=AUTO_V       if = y, auto adjust min_v and max_v (default:0),
                        affect for eqw, and others in scaling
  --mode_pre_img=MODE_PRE_IMG
                        support caffe/tf (default:caffe)
  --channel=CHANNEL     channel of images, 1: gray, 2: color (default:3)
  -m DIM_IMG, --dim_img=DIM_IMG
                        width or height (square) of images, -1: get real size
                        of original images (default:-1)
  -v VISUALIZE_MODEL, --visualize_model=VISUALIZE_MODEL
                        visualize the model if > 0 (default:0)
  --algo_redu=ALGO_REDU
                        algorithm of dimension reduction (rd_pro/pca/fa),  if
                        emtpy so do not use (default:)
  --reduc_perle=REDUC_PERLE
                        perlexity for tsne (default:10)
  --reduc_ini=REDUC_INI
                         ini for reduction (default:pca) of data (only use for
                        fillup) (default:none)
  -t TYPE_EMB, --type_emb=TYPE_EMB
                        type of the embedding (default:raw):
                        raw/bin/fill/fills/zfill/zfills/tsne
  --imp_fea=IMP_FEA     using important features for overlapped issues
                        (default:none/rf/avg/max)
  -g LABEL_EMB, --label_emb=LABEL_EMB
                        taxa level of labels provided in supervised embeddings
                        kingdom=1,phylum=2,class=3,order=4,family=5, genus=6
                        (default:0)
  --emb_data=EMB_DATA   data used for embbed with dimensionality reduction: :
                        transformed data; o: original data
  -y TYPE_BIN, --type_bin=TYPE_BIN
                        type of binnings: spb/eqw/pr/eqf (default:)
  -p PERLEXITY_NEIGHBOR, --perlexity_neighbor=PERLEXITY_NEIGHBOR
                        perlexity for tsne/#neighbors for others (default:5)
  --n_components_emb=N_COMPONENTS_EMB
                        ouput after embedding (default:2)
  -s SHAPE_DRAWN, --shape_drawn=SHAPE_DRAWN
                        shape of point to illustrate data:
                        (pixel)/ro/o(circle) (default:,)
  --fig_size=FIG_SIZE   fig_size to contain all features, if 0:smallest which
                        fit data,  (default:0)
  --point_size=POINT_SIZE
                        point size for img (default:1)
  --colormap=COLORMAP   colormaps for generating images (rainbow
                        /nipy_spectral/jet/Paired/Reds/YlGnBu)
                        (default:custom)
  --margin=MARGIN       margin to images (default:0)
  --alpha_v=ALPHA_V     1 (opaque) (default:1)
  --recreate_img=RECREATE_IMG
                         if >0 rerun to create images even though they are
                        existing (default:0)

```

Some examples as below:

## Available Datasets

![Information on datasets](images/datasets.jpg)

## The framework, in default, run 10 times with 10-stratified-cross-validation
** NOTES: 
1. Select run on GPU, set cudaid in (0,1,2,3) (id of GPU on machine, id=-1 means use of cpu). Note: your computation nodes must be supported with GPU and installed Tensorflow GPU.
2. Select dataset with parameter '-i', eg. '-i cirphy' (phylogenetic cirrhosis dataset)
3. Select model with parameter '--model', eg. '--model model_cnn'. Default: The model with one Fully connected layer (FC) model
4. Other parameters, One can refer at the function para_cmd()

## Code to run experiment (for raw data)

Parameters: -n: number of convolutional layers, -f : number of filters, 
-t: type of embeddings (suporting raw-1D and images 2D such as fillup, t-sne, isomap, lda,....)
```
db='wt2dphy';
python3 -m deepmg -i $db -t raw 
python3 -m deepmg -i $db -t raw --model model_cnn1d -n 1 -f 64 
```

## Code to run experiment (for fill-up with gray images)
use SPB
```
db='wt2dphy';
python3 -m deepmg -i $db -t fill -y spb  -z 255 --colormap gray --channel 1
python3 -m deepmg -i $db -t fill -y spb  -z 255 --colormap gray --channel 1 --model model_cnn -n 1 -f 64 
```
use PR
```
db='wt2dphy';
python3 -m deepmg -i $db -t fill -y pr  -z 255 --colormap gray --channel 1
```
use QTF (with eqw binning)
```
db='wt2dphy';
python3 -m deepmg -i $db -t fills -y eqw --scale_mode qtf --auto_v y   -z 255 --colormap gray --channel 1
```

## Code to run experiment (for fill-up with color images)
```
db='wt2dphy';
python3 -m deepmg -i $db -t fill -y spb -z 255 --preprocess_img vgg16 --colormap jet_r
```

## Code to run experiment with visualizations based on manifold learning, e.g, t-sne (changed the parameter of '-t' to 'tsne')
We are also able to test another embeddings such isomap, lle,... 
We use images of 24x24 (--fig_size 24) and transparent rate (alpha_v = 0.5)
```
db='wt2dphy';
python3 -m deepmg -i $db -t tsne -y spb --fig_size 24 -z 255 --colormap gray --channel 1 --alpha_v 0.5
```

## Scripts (\*.sh) in details provided in [utils/scripts](./utils/scripts/) with:
The scripts mostly are used for datasets in group A (if not specified) including predicting cirrhosis, colorectal, IBD, obesity, T2D (and WT2D dataset). The header part of each file consists of the information on memory, number of cores, walltime, email, etc. which used in job schedulers. These parameters should be modified depending on your available resources. Each file runs numerous models for one dataset.

Scripts for 6 datasets (files: cirphy_\* (cirphy_x.csv for data and cirphy_y.csv for labels, in order to run training on this dataset set the parameter -i, eg. "-i cirphy"), colphy_\*, ibdphy_\*, obephy_\*, t2dphy_\*, wt2dphy_\*) in group A [MetAML] (https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004977):

* *1d*: scripts for running models with 1D data
* *manifold_iso*: training species abundance using visualizations based on Isomap.
* *manifold_mds*: training species abundance using visualizations based on MDS.
* *manifold_nmf*: training species abundance using visualizations based on NMF.
* *manifold_pca*: training species abundance using visualizations based on PCA.
* *manifold_lda1*,2,3,4,5,6: training species abundance using visualizations based on LDA (supervised) with labels using various levels of OTUs (1: Kingdom, 2: Phylum, 3: Class,4: Order,5: Family and 6: genus).
* *phy0_24_cmap_r*: investigate a vast of colormaps (viridis, rainbow, jet,...)
* phyfill0_vgg: investigate various paramters of VGG architectures.
* *fill0cnn*: run experiments using Fill-up with different CNN hyper-parameters.
* *phyfill0_rnd*: the experiments using Fill-up with random feature ordering 

Scripts training datasets for other groups:

* *gene_fill*: training gene families abundance (names: cirgene, colgene, ibdgene, obegene, t2dgene, wt2dgene) with Fill-up and *machine_learning_gene*: training gene families abundance with stardard learning algorithms (SVM, RF).
* *phyfill0_CRC*: experiments on datasets (yu, feng, zeller, vogtmann, crc) in the paper [Multi-cohort analysis of colorectal cancer metagenome identified altered bacteria across populations and universal bacterial](https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-018-0451-2)
* *phyfill0_phcnn*: experiments on datasets (files: ibdtrainHS_CDf, ibdtrainHS_CDr, ibdtrainHS_iCDf, ibdtrainHS_iCDr, ibdtrainHS_UCf, ibdtrainHS_UCr)in the paper [Phylogenetic convolutional neural networks in metagenomics](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2033-5)
* *balance_phyfill0* (for color images) and *balance_phygrayfill0* (for gray images): experiments on datasets (hiv, crohn) in the paper [Balances: a New Perspective for Microbiome Analysis](https://msystems.asm.org/content/3/4/e00053-18)


# Utilities and visualizations

## Visualize models by ASCII
Just add "-v 1" to visualize the network. In order to use this feature, please install 'keras_sequential_ascii'

```
db='wt2dphy';
size_img=0;
python3 -m deepmg -i $db -t fill -y spb  -z 255 --colormap gray --channel 1 -v y
python3 -m deepmg -i $db -t fill -y spb  -z 255 --colormap gray --channel 1 --model model_cnn -n 1 -f 64 -v y
```

## Jupyter: Visualization of representations
Please move to **./utils/jupyter/** to visualize representations based on images:

```
utils/jupyter/
sudo jupyter notebook --allow-root
```

* [compare_manifolds.ipynb](./utils/jupyter/compare_manifolds.ipynb) : visualizations generated from manifold learning such as t-SNE, LDA, Isomap
* [plot_distribution_taxa_levels_colormaps.ipynb](./utils/jupyter/plot_distribution_taxa_levels_colormaps.ipynb) : show how fill-up works and visualize important features using fill-up
* [visual_fillup_colormaps.ipynb](./utils/jupyter/visual_fillup_colormaps.ipynb) : illustrate various colormaps
* [vis_explanations_cnn_LIME_GRAD.ipynb](./utils/jupyter/vis_explanations_cnn_LIME_GRAD.ipynb) : exhibit explanations by Saliency, LIME and Grad-Cam

# Summarize the results

Some tools are available in this project **(./utils/read_results)** supporting to collect the data, filter the results, and delete uncompleted experiments
* [read_results.py](./utils/read_results/read_results.py): collect all experiments with:
  - each row presenting the average performance in ACC, AUC, MCC, f1-score, execution time... (results_sum.txt)
  - each row presenting a fold of a experiment in ACC, AUC, MCC, confusion matrix... (results_folds.txt)
  - each row presenting a result in external validation of a experiment in ACC, AUC, MCC, confusion matrix... (results_ext.txt)
* [unfi_delete.py](./utils/read_results/unfi_delete.py): delete/count uncompleted log files of unfinished experiments.

# Authors

* **Thanh Hai Nguyen** (E-mail: hainguyen579 [at] gmail.com or nthai [at] cit.ctu.edu.vn) 
* **Edi Prifti** (E-mail: e.prifti [at] ican-institute.org) 
* **Nataliya Sokolovska** (E-mail: nataliya.sokolovska [at] upmc.fr) 
* **Jean-daniel Zucker** (E-mail: jean-daniel.zucker [at] ird.fr) 

