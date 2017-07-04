![](https://www2.cisl.ucar.edu/sites/default/files/users/bjsmith/Cheyenne-450.jpg)

# Cheyenne

Cheyenne is a **5.34-petaflops**, high-performance computer built for NCAR.

## Features of Cheyenne


- **145 152 processor cores**   
  - 2.3- GHz Intel Xeon processors 
  - 16 flops per clock 

- **4 032 computation nodes**  
  - Dual-socket nodes 
  - 18 cores per socket             

- **6 login nodes**   
  - Dual-socket nodes 
  - 18 cores per socket 
  - 256 GB memory/node                        

- **313 TB total system  memory** 
  - 64 GB/node on 3,168 nodes, DDR4-2400 
  - 128 GB/node on 864 nodes, DDR4-2400        

- **Mellanox EDR InfiniBandhigh-speed  interconnect**
   - Partial 9D Enhanced Hypercube single-plane interconnect topology 
   - Bandwidth: 25 GBps bidirectional per link 
   - Latency: MPI ping-pong < 1 µs; hardware link 130 ns 

- **3 times Yellowstone computational  capacity**  
- **> 3.5 times Yellowstone peak  performance**  
  - 5.34 peak petaflops (vs. 1.504) 

## Data Analysis and Visualization 
- Geyser
 - 16 Quad-socket nodes
 - 10-core westermer
 - 1 TB Memory

- Caldera


## File Storage 

- Glade Parallel spinning disk storage
 - Uses IBM GPFS/Spectrum Scale Technology
 - Optimized for parallel I/O operations
 - Simulation and analysis I/O occurs here

- HPSS tape archive
 - POSIX-like interface for long term aarchival and data backups
 - Data must be sent and received to tape - not available on demand

All storage is shared between YS and CH!


