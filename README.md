## hf2hd-demo

to make sample workspace do:
    
    ./make_data.py
    hist2workspace config/simple.xml
    ./make_fake_data.py
    hist2workspace config/simple.xml

to produce sample plots and histfactory outputs

    ./demo_plot.py config/simple.xml channel1 plot.png
    ./demo_hepdata.py config/simple.xml channel1 data12.yaml

