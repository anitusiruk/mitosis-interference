"""Score ablation: pre-update prediction loss, frozen prospective harm guards."""
import copy
from src.adapter_pool_cau_v1 import CAUV1AdapterPool
from src.adapter_pool_head_only import HeadOnlyCAUV1AdapterPool


def initial_loss_scores(original):
    if original.get('status')!='ok':return original
    result=copy.deepcopy(original)
    result['scoring_policy']='pre_update_query_loss_ablation'
    result['original_post_update_fresh_utility']=result['fresh_utility']
    result['original_post_update_best_reuse']=result['best_reuse']
    result['original_post_update_best_reuse_utility']=result['best_reuse_utility']
    for key in ['fold_a_fresh_utility','fold_b_fresh_utility']:
        if key in result:result['original_post_update_'+key]=result.pop(key)
    for profile in result['reuse_profiles'].values():
        profile['original_post_update_system_utility']=profile['system_utility']
        profile['system_utility']=result['statusquo_loss']-profile['query_before']
        for key in ['fold_a_utility','fold_b_utility']:
            if key in profile:profile['original_post_update_'+key]=profile.pop(key)
    feasible=[n for n,p in result['reuse_profiles'].items() if p['feasible_both']]
    best=min(feasible,key=lambda n:(-result['reuse_profiles'][n]['system_utility'],
             result['reuse_profiles'][n]['harm_lcb_max'],result['reuse_profiles'][n]['harm_mean'],n)) if feasible else None
    best_utility=result['reuse_profiles'][best]['system_utility'] if best is not None else None
    result['best_reuse']=best;result['best_reuse_utility']=best_utility
    result['best_reuse_query_after']=result['reuse_profiles'][best]['query_after'] if best is not None else None
    result['best_reuse_query_before']=result['reuse_profiles'][best]['query_before'] if best is not None else None
    result['fresh_utility']=result['statusquo_loss']-result['fresh_query_before']
    result['fresh_advantage']=result['fresh_utility']-best_utility if best is not None else None
    result['fresh_positive']=result['fresh_utility']>0 and (best is None or result['fresh_utility']>best_utility)
    return result


class InitialLossScoreMixin:
    def crossfit_action_utility(self,*args,**kwargs):
        return initial_loss_scores(super().crossfit_action_utility(*args,**kwargs))


class InitialLossCAUV1AdapterPool(InitialLossScoreMixin,CAUV1AdapterPool):pass
class InitialLossHeadOnlyCAUV1AdapterPool(InitialLossScoreMixin,HeadOnlyCAUV1AdapterPool):pass
