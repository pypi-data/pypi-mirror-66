import os
import pathlib

import numpy as np

import lsmtool
lsmtool.logger.setLevel('warning')

from . import utils, msutils, worker, flagutils

cwd = os.getcwd()


def get_cal_config(name):
    return pathlib.Path(__file__).absolute().parent / 'cal_config' / name


class SkyModel(object):

    def __init__(self, app_sourcedb_name, ateam_bbs_name):
        self.app_sourcedb = app_sourcedb_name
        self.ateam_bbs = ateam_bbs_name
        self.ateam_stat_cache = dict()

    def get_sky_model(self, msin):
        return f'{msin}/sky_model/{self.app_sourcedb}'

    def get_ateam_sky_model(self, msin):
        return f'{msin}/sky_model/{self.ateam_bbs}'

    def get_ateam_stat(self, msin):
        if msin not in self.ateam_stat_cache:
            model = lsmtool.load(self.get_ateam_sky_model(msin))
            s = dict(zip(model.getPatchNames(), model.getColValues('I', aggregate='sum'))), model.getPatchPositions()
            self.ateam_stat_cache[msin] = s
        return self.ateam_stat_cache[msin]

    def get_patch_i(self, msin, patch):
        if isinstance(patch, str):
            return self.get_ateam_stat(msin)[0][patch]
        return sum(self.get_patch_i(msin, k) for k in patch)

    def get_patch_coord(self, msin, patch):
        return self.get_ateam_stat(msin)[1][patch]

    def get_patchs(self, msin, include_main=True, exclude=None):
        ateams = self.get_ateam_stat(msin)[0]
        patches = sorted(ateams, key=ateams.get, reverse=True)
        if include_main:
            patches.append('Main')
        if exclude:
            for patch in exclude:
                if patch in patches:
                    patches.remove(patch)
        return patches

    def get_directions(self, msin, dir_name_or_idx, include_main=True):
        patchs = self.get_patchs(msin, include_main=include_main)
        dirs = []
        if isinstance(dir_name_or_idx, (int, slice)):
            dirs = patchs[dir_name_or_idx]
        elif dir_name_or_idx == 'all':
            dirs = patchs
        elif dir_name_or_idx in patchs:
            dirs = [dir_name_or_idx]
        return dirs

    def copy(self, msins, msouts):
        utils.zip_copy(msins, msouts, self.get_sky_model(''))
        utils.zip_copy(msins, msouts, self.get_ateam_sky_model(''))


class CalSettings(object):

    def __init__(self, parmdb='instrument.h5', sol_int=1, sol_int_flux_per_slot_per_sec=None,
                 sol_int_min=2, sol_int_max=120, cal_mode='fulljones', uv_min=None, **extra_param):
        self.parmdb = parmdb
        self.sol_int = sol_int
        self.cal_mode = cal_mode
        self.uv_min = uv_min
        self.extra_param = extra_param
        self.sol_int_min = sol_int_min
        self.sol_int_max = sol_int_max
        self.sol_int_flux_per_slot_per_sec = sol_int_flux_per_slot_per_sec
        self.freq_cache = {}
        self.interval_cache = {}

    def get_time_interval(self, msin):
        if msin not in self.interval_cache:
            self.interval_cache[msin] = msutils.get_ms_time_interval(msin)
        return self.interval_cache[msin]

    def get_freq(self, msin):
        if msin not in self.freq_cache:
            self.freq_cache[msin] = msutils.get_ms_freqs(msin)
        return self.freq_cache[msin]

    def get_uv_min(self, msin):
        if not self.uv_min:
            return self.uv_min
        if isinstance(self.uv_min, float, int):
            return self.uv_min
        fmhz = self.get_freq(msin) * 1e-6
        fmhzs, lims = list(zip(*sorted(self.uv_min.items())))
        i = np.where(np.array(fmhzs) - fmhz >= 0)[0][0]
        return lims[i]

    def get_sol_int(self, msin, patch_i):
        if self.sol_int_flux_per_slot_per_sec is None:
            return int(self.sol_int)

        int_time = self.get_time_interval(msin)
        b = (self.sol_int_flux_per_slot_per_sec / patch_i / int_time)
        if b >= self.sol_int_max:
            return self.sol_int_max
        f = utils.factors(self.sol_int_max)
        c = f[(f - b) > 0][0]
        return int(max(self.sol_int_min, c))


class MultiCommands(object):

    def __init__(self, worker_settings, name, max_time=None):
        self.worker_settings = worker_settings
        self.name = name
        self.max_time = max_time

    def build_command(self, msin, parameters):
        raise NotImplementedError()

    def get_parameters(self, msin):
        return []

    def get_out_file(self, msin):
        return msin

    def run(self, in_files):
        print(f'Starting {self.name} ...')
        pool = worker.get_worker_pool(self.name, max_time=self.max_time, **self.worker_settings)
        out_files = []

        for in_file in in_files:
            in_file = os.path.normpath(in_file)
            parameters = self.get_parameters(in_file)
            out_file = self.get_out_file(in_file)
            if parameters is None:
                print(f'Skipping {in_file}')
                continue
            cmd = self.build_command(in_file, parameters)
            # pool.add(f'echo "{cmd}"')
            pool.add(cmd)
            out_files.append(out_file)

        pool.execute()

        return out_files


class AoQuality(MultiCommands):

    def __init__(self, worker_settings, max_time=None):
        MultiCommands.__init__(self, worker_settings, 'AoQuality', max_time=max_time)

    def build_command(self, msin, parameters):
        return f'cd {cwd}; aoquality collect {msin} '


class PlotSolutions(MultiCommands):

    def __init__(self, worker_settings, parmdb_in_name, clip=False):
        self.parmdb_in_name = parmdb_in_name
        self.clip = clip
        MultiCommands.__init__(self, worker_settings, 'PlotSol')

    def get_parameters(self, msin):
        parmdb = f'{msin}/{self.parmdb_in_name}'
        if not os.path.exists(parmdb):
            return None
        p = [parmdb, ]
        if self.clip:
            p.append('--clip')
        return p

    def build_command(self, msin, parameters):
        parameters = ' '.join(parameters)
        return f'cd {cwd}; soltool plot {parameters}'


class CopyFlag(MultiCommands):

    def __init__(self, worker_settings, in_postfix, out_postfix):
        self.in_postfix = in_postfix
        self.out_postfix = out_postfix
        MultiCommands.__init__(self, worker_settings, 'CopyFlag')

    def build_command(self, msin, parameters):
        ms_flag = f'_{self.in_postfix}.MS'.join(msin.rsplit(f'_{self.out_postfix}.MS', 1))
        return f'cd {cwd}; flagtool copy {ms_flag} {msin}'


class DPPP(MultiCommands):

    def __init__(self, worker_settings, name, parset, max_time=None):
        self.parset = parset
        MultiCommands.__init__(self, worker_settings, name, max_time=max_time)

    def build_command(self, msin, parameters):
        log_dir = f'{os.path.dirname(msin)}/logs/'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_name = self.name.replace(' ', '_').lower()
        log_file = f'{log_dir}/{os.path.basename(msin)}_{log_name}.log'
        parameters = ' '.join(parameters)

        return f'cd {cwd}; DPPP {self.parset} msin={msin} {parameters} |tee {log_file}'

    def get_directions_str(self, directions):
        return '[%s]' % ','.join(['[%s]' % k for k in directions])


class CopyDataCol(DPPP):

    def __init__(self, worker_settings, col_in, col_out):
        self.col_in = col_in
        self.col_out = col_out
        DPPP.__init__(self, worker_settings, 'CopyCol', '')

    def get_parameters(self, msin):
        return ['numthreads=200', f'msin={msin}', f'msin.datacolumn={self.col_in}',
                f'msout=.', f'msout.datacolumn={self.col_out}', 'steps=[]']


class CopyMS(DPPP):

    def __init__(self, worker_settings, col_in, ms_out_postfix):
        self.col_in = col_in
        self.postfix = ms_out_postfix
        DPPP.__init__(self, worker_settings, 'CopyMS', '')

    def get_out_file(self, msin):
        return f'_{self.postfix}.MS'.join(msin.rsplit('.MS', 1))

    def get_parameters(self, msin):
        msout = self.get_out_file(msin)
        return ['numthreads=200', 'msout.overwrite=true', f'msin={msin}', f'msin.datacolumn={self.col_in}',
                f'msout={msout}', f'msout.datacolumn=DATA', 'steps=[]']


class DDEcal(DPPP):

    def __init__(self, worker_settings, cal_settings, sky_model, data_col='DATA', directions='all'):
        self.settings = cal_settings
        self.sky_model = sky_model
        self.directions = directions
        self.data_col = data_col

        DPPP.__init__(self, worker_settings, 'DDEcal', get_cal_config('dppp_ddcal_ateam.parset'))

    def get_parameters(self, msin):
        parmdb_out = f'{msin}/{self.settings.parmdb}'

        if os.path.exists(parmdb_out):
            os.remove(parmdb_out)

        directions = self.sky_model.get_directions(self.directions)

        sol_int = self.settings.get_sol_int(msin, self.sky_model.get_patch_i(msin, directions))

        p = []
        p.append(f'msin.datacolumn={self.data_col}')
        p.append(f'msout.datacolumn={self.data_col}')
        p.append(f'cal.sourcedb={self.sky_model.get_sky_model(msin)}')
        p.append(f'cal.directions={self.get_directions_str(directions)}')
        p.append(f'cal.h5parm={parmdb_out}')
        p.append(f'cal.solint={sol_int}')
        p.append(f'cal.mode={self.settings.cal_mode}')

        for k, v in self.settings.extra_param.items():
            p.append(f'cal.{k}={v}')

        if not self.settings.uv_min:
            p.append(f'cal.uvlambdamin={self.settings.get_uv_min(msin)}')

        return p


class DDEcalAvg(DDEcal):

    def __init__(self, worker_settings, cal_settings, sky_model, time_avg=4, freq_avg=4):
        DDEcal.__init__(self, worker_settings, cal_settings, sky_model)
        self.time_avg = time_avg
        self.freq_avg = freq_avg

    def get_out_file(self, msin):
        p = pathlib.Path(msin)
        return str(p.parent / ('tmp_' + p.name))

    def get_parameters(self, msin):
        msout = self.get_out_file(msin)

        p = DDEcal.get_parameters(self, msin)
        p.append('steps=[avg,cal]')
        p.append('avg.type=averager')
        p.append(f'avg.timestep={self.time_avg}')
        p.append(f'avg.freqstep={self.freq_avg}')
        p.append(f'msout={msout}')
        p.append(f'msout.overwrite=true')

        return p


class Subtract(DPPP):

    def __init__(self, worker_settings, cal_settings, sky_model, col_in, col_out, directions='all', max_time=240):
        self.settings = cal_settings
        self.sky_model = sky_model
        self.col_in = col_in
        self.col_out = col_out
        self.directions = directions

        cal_file = 'dppp_subtract.parset'
        if self.settings.cal_mode == 'diagonal':
            cal_file = 'dppp_subtract_diag.parset'

        DPPP.__init__(self, worker_settings, 'Subtract', get_cal_config(cal_file), max_time=max_time)

    def get_parameters(self, msin):
        directions = self.sky_model.get_directions(self.directions)
        if not directions:
            return None

        p = []
        p.append(f'msin.datacolumn={self.col_in}')
        p.append(f'msout.datacolumn={self.col_out}')
        p.append(f'sub.sourcedb={self.sky_model.get_sky_model(msin)}')
        p.append(f'sub.directions={self.get_directions_str(directions)}')
        p.append(f'sub.applycal.parmdb={msin}/{self.settings.parmdb}')

        return p


class SubtractAteam(Subtract):

    def __init__(self, worker_settings, cal_settings, sky_model, col_in, col_out, max_time=240):
        Subtract.__init__(self, worker_settings, cal_settings, sky_model, col_in, col_out,
                          directions=slice(None, -1), max_time=max_time)


class Peel(object):

    def __init__(self, sky_model):
        self.sky_model = sky_model

    def iterations(self, msins):
        n_pactchs = np.array([len(self.sky_model.get_patchs(msin, include_main=False)) for msin in msins])
        for i in np.arange(1, max(n_pactchs) + 1):
            return i, msins[n_pactchs >= i]


class PeelPreSubtract(Subtract):

    def __init__(self, peel_iter, worker_settings, cal_settings, sky_model, col_in='DATA', max_time=240):
        Subtract.__init__(self, worker_settings, cal_settings, sky_model, col_in, 'DATA_PEEL',
                          directions=slice(peel_iter, None), max_time=max_time)
        self.name = f'PeelPreSub {peel_iter}'
        self.peel_iter = peel_iter


class PeelCal(DDEcal):

    def __init__(self, peel_iter, worker_settings, cal_settings, sky_model):
        DDEcal.__init__(self, worker_settings, cal_settings, sky_model, data_col='DATA_PEEL',
                        directions=peel_iter - 1)
        self.name = f'PeelCal {peel_iter}'
        self.peel_iter = peel_iter


class PeelPostSubtract(Subtract):

    def __init__(self, peel_iter, worker_settings, cal_settings, sky_model, data_col='DATA', max_time=240):
        Subtract.__init__(self, worker_settings, cal_settings, sky_model, data_col, data_col,
                          directions=peel_iter - 1, max_time=max_time)
        self.name = f'PeelPostSub {peel_iter}'
        self.peel_iter = peel_iter


class PeelPreSubtractPhaseShifted(PeelPreSubtract):

    def __init__(self, peel_iter, worker_settings, cal_settings, sky_model, col_in='DATA',
                 max_time=240, time_avg=4, freq_avg=4):
        PeelPreSubtract.__init__(self, peel_iter, worker_settings, cal_settings, sky_model,
                                 col_in=col_in, max_time=max_time)
        self.time_avg = time_avg
        self.freq_avg = freq_avg

    def get_out_file(self, msin):
        p = pathlib.Path(msin)
        return str(p.parent / ('tmp_' + p.name))

    def get_parameters(self, msin):
        coord = self.sky_model.get_patch_coord(msin, self.peel_iter - 1)
        msout = self.get_out_file(msin)

        p = PeelPreSubtractPhaseShifted.get_parameters(self, msin)
        p.append('steps=[sub,phaseshift,avg]')
        p.append('phaseshift.type = phaseshifter')
        p.append('avg.type = average')
        p.append(f'phaseshift.phasecenter=[{coord[0].deg}deg,{coord[1].deg}deg]')
        p.append(f'avg.timestep={self.time_avg}')
        p.append(f'avg.freqstep={self.freq_avg}')
        p.append(f'msout={msout}')

        return p


class PeelPostSubtractPhaseShift(PeelPostSubtract):

    def __init__(self, peel_iter, worker_settings, cal_settings, sky_model, data_col='DATA', max_time=None,
                 coord_phase_back=None):
        PeelPostSubtract.__init__(self, peel_iter, worker_settings, cal_settings, sky_model,
                                  data_col=data_col, max_time=max_time)
        self.coord_phase_back = coord_phase_back

    def get_out_file(self, msin):
        p = pathlib.Path(msin)
        return str(p.parent / ('tmp_' + p.name))

    def get_parameters(self, msin):
        coord = self.sky_model.get_patch_coord(msin, self.peel_iter - 1)
        msout = self.get_out_file(msin)

        if self.coord_phase_back:
            coord_phase_back = f'[{self.coord_phase_back.ra.deg}deg,{self.coord_phase_back.dec.deg}deg]'
        else:
            coord_phase_back = '[]'

        p = PeelPostSubtract.get_parameters(self, msin)
        p.append('steps=[phaseshift,sub,phaseshiftback]')
        p.append('phaseshift.type = phaseshifter')
        p.append('phaseshiftback.type = phaseshifter')
        p.append(f'phaseshift.phasecenter=[{coord[0].deg}deg,{coord[1].deg}deg]')
        p.append(f'phaseshiftback.phasecenter={coord_phase_back}')
        p.append(f'msout={msout}')

        return p


class ApplyCal(DPPP):

    def __init__(self, worker_settings, cal_settings, col_in='DATA',
                 col_out='CORRECTED_DATA', direction='Main'):
        self.col_in = col_in
        self.col_out = col_out
        self.direction = direction
        self.settings = cal_settings
        self.direction = direction
        dppp_file = 'dppp_applycal.parset'
        if self.settings.cal_mode == 'diagonal':
            dppp_file = 'dppp_applycal_diag.parset'

        DPPP.__init__(self, worker_settings, 'ApplyCal', get_cal_config(dppp_file))

    def get_parameters(self, msin):
        p = []
        p.append(f'apply.parmdb={msin}/{self.settings.parmdb}')
        p.append(f'apply.direction=[{self.direction}]')
        p.append(f'msin.datacolumn={self.col_in}')
        p.append(f'msout.datacolumn={self.col_out}')

        return p


class FlagPostCal(DPPP):

    def __init__(self, worker_settings, postfix='002', strategy='nenufar_1s1c'):
        if strategy == 'nenufar_1s1c':
            strategy = get_cal_config(strategy)
        self.strategy = strategy
        self.postfix = postfix
        DPPP.__init__(self, worker_settings, 'FlagPostCal', get_cal_config('dppp_flagger.parset'))

    def get_out_file(self, msin):
        return f'_{self.postfix}.MS'.join(msin.rsplit('.MS', 1))

    def get_parameters(self, msin):
        p = []
        p.append(f'flag.strategy={self.strategy}')
        p.append(f'msout={self.get_out_file(msin)}')

        return p


class FlagBadStations(DPPP):

    def __init__(self, worker_settings, nsigma=5):
        self.nsigma = nsigma
        DPPP.__init__(self, worker_settings, 'FlagBadStations', get_cal_config('dppp_preflag_baselines.parset'))

    def get_parameters(self, msin):
        to_flag = flagutils.get_badstatsions(msin, self.nsigma)
        if len(to_flag) == 0:
            return None

        to_flag = ','.join([str(k) for k in to_flag])
        return [f'flag.baseline={to_flag}']


class FlagBadBaselines(DPPP):

    def __init__(self, worker_settings, nsigma=5, nsigma_baselines=8):
        self.nsigma = nsigma
        self.nsigma_baselines = nsigma_baselines
        DPPP.__init__(self, worker_settings, 'Flag Bad Stations', get_cal_config('dppp_preflag_baselines.parset'))

    def get_parameters(self, msin):
        to_flag = flagutils.get_badbaselines(msin, self.nsigma, self.nsigma_baselines)
        if len(to_flag) == 0:
            return None

        return [f'flag.baseline="{to_flag}"']


class SSINSFlagger(MultiCommands):

    def __init__(self, worker_settings, config=None, plot_dir=None):
        self.config = config
        self.plot_dir = plot_dir
        MultiCommands.__init__(self, worker_settings, 'SSINS')

    def get_parameters(self, msin):
        p = []
        if self.plot_dir is not None:
            p.append(f'--plot_dir={os.path.join(msin, self.plot_dir)}')
        if self.config is not None:
            p.append(f'--config={self.config}')
        return p

    def build_command(self, msin, parameters):
        return f'cd {cwd}; flagtool ssins {msin} {" ".join(parameters)}'


class TestMulti(MultiCommands):

    def __init__(self, worker_settings, name):
        MultiCommands.__init__(self, worker_settings, name)

    def get_parameters(self, msin):
        p = []
        p.append(f'in_file={msin}')
        return p

    def get_out_file(self, msin):
        return '_002.MS'.join(msin.rsplit('.MS', 1))

    def build_command(self, msin, parameters):
        parameters = ' '.join(parameters)
        return f'echo {msin} {parameters}'


def main():
    pass

    # ret = TestMulti('test').run(msins)
    # print(ret)

    # AoQuality().run(msins)
    # PostProcessSolutions('instru_test.h5').run(msins)

    # CopyDataCol('DATA', 'SUBTRACTED_DATA').run(msins)

    # for i in range(3):
    #     parmdb_iter = f'instrument_peel_iter{i + 1}.h5'
    #     PeelCalibrate(i + 1, 'instrument_smooth.h5', parmdb_iter, sol_int_fct).run(msins)
    #     PostProcessSolutions(parmdb_iter).run(msins)
    #     PeelSubtract('SUBTRACTED_DATA', 'SUBTRACTED_DATA', parmdb_iter, i + 1).run(msins)

    # ApplyCal('SUBTRACTED_DATA', 'CORRECTED_DATA', 'instrument_smooth.h5', 'Main').run(msins)
    # AoQuality().run(msins)

    # FlagPostCal().run(msins)


if __name__ == '__main__':
    main()
