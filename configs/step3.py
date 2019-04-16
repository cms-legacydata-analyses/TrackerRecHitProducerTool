import FWCore.ParameterSet.Config as cms

process = cms.Process("Savehits")

process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load("RecoTracker.TrackProducer.TrackRefitters_cff") 

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V27::All', '')
process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/START53_V27.db')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:step2.root'
    )
)

process.load("RecoLocalTracker.SiPixelRecHits.SiPixelRecHits_cfi")
process.load("RecoLocalTracker.SiStripRecHitConverter.SiStripRecHitConverter_cfi")

process.demo = cms.EDAnalyzer('SaveHits',

   associateRecoTracks = cms.bool(True),
   associateHitbySimTrack = cms.bool(True),
   associatePixel = cms.bool(True),       
   associateStrip = cms.bool(True),
   pixelSimLinkSrc = cms.InputTag("simSiPixelDigis"),
   stripSimLinkSrc = cms.InputTag("simSiStripDigis"),
   ROUList = cms.vstring('TrackerHitsPixelBarrelLowTof',
                         'TrackerHitsPixelBarrelHighTof',
                         'TrackerHitsPixelEndcapLowTof',
                         'TrackerHitsPixelEndcapHighTof',
                         'TrackerHitsTIBLowTof',
                         'TrackerHitsTIBHighTof',
                         'TrackerHitsTIDLowTof',
                         'TrackerHitsTIDHighTof',
                         'TrackerHitsTOBLowTof',
                         'TrackerHitsTOBHighTof',
                         'TrackerHitsTECLowTof',
                         'TrackerHitsTECHighTof'),

   TrackerRecHitBuilder = cms.string('WithAngleAndTemplate')

)


process.p = cms.Path(process.siStripMatchedRecHits*process.siPixelRecHits*process.TrackRefitter*process.demo)
process.schedule = cms.Schedule(process.p)
