When downloading datasets (see datasets.py), the following file *.openbis_datasets.json* should be written in the CWD:

```
{
  "openbis-tst.ethz.ch": {
    "datasets": {
      "20190403103900470-570": {
        "sftp_path": "/SIS_VERMEUL/MY-FIRST-PROJECT/MY-FIRST-PROJECT_EXP_1/20190403103900470-570",
        "nfs_path": "3FD2018F-1AC7-4187-8653-AC51E478D03E/69/44/5b/20190403103900470-570",
        "target_dir": "data/my_dataset_1",
        "type": "symlink"
      },
      "20200204153400101-4972": {
        "sftp_dir": "/SIS_VERMEUL/MY-FIRST-PROJECT/MY-FIRST-PROJECT_EXP_1/20200204153400101-4972/original",
	"location": "3FD2018F-1AC7-4187-8653-AC51E478D03E/69/44/5b/20200204153400101-4972/original"
        "target_dir": "data/my_other_dataset",
        "type": "physical"
      },
      "20200204153516069-001": {
        "target_dir": "data/my_new_dataset",
        "type": "new"
      }
    }
  }
}
```

* every openBIS dataStore hostname is one key
* every permId is a key inside a dataStore
* *sftp_path* is the path to the dataSet in a sftp-mounted dataStore (via FUSE/SSHFS)
* *nfs_path* is the path to the dataSet in a NFS-mounted dataStore. It is equal to the *location* attribute of a dataSet
* the *target_dir* is relative to the CWD (current working directory) and represents either the symbolic link or the physical data
* when downloading files, a *destination* attribute can be specified, which is equal to *target_dir*. It defaults to *hostname/permId*

* in general, all SSHFS mountpoints should mount to the root of the dataStore
* from a given dataSet *permId*, its *experiment/collection*, *project* and *space* form the location inside the SSHFS mountpoint:
* /SPACE/PROJECT/EXPERIMENT/permId
* in offline mode, symlinks should be replaced by physical downloads
* a method *openbis.work_offline()* should be provided, which reads the file above and converts all symbolic links to real directories
* after the successful download of a dataset, the file *.openbis_datasets.json* should be updated
* for future: new datasets could be created, using the local timestamp to create a unique permId:
* from datetime import datetime
* datum.strftime('%Y%m%d%H%M%S%f') + "-001"
* another method *openbis.work_online()* should automatically upload new dataSets to openBIS.