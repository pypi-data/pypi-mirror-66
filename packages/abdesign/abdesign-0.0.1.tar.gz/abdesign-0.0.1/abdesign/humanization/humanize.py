from abdesign.util.annotation import _all_params_present
from abdesign.core.igobject import IgObject

# TODO: REFACTOR REPLACEMENT
def replace_cdr(igquery: IgObject,igtarget: IgObject, annotation_type):
    """Function which gets two IgObjects (Query and Target) and generates a new hybrid IgObject.
    

    Parameters
    ----------
    igquery : IgObject
        Object representing the Query-Sequence which is annotated and contains CDRs. CDRs from this object 
        were extracted and integrated in FR regions from Target region.
    igtarget : IgObject
        Object representing the Target-Sequence which is annotated and contains FR.
    annotation_type : string
        String representing an annotation type. 
    
    Returns
    -------
    IgObject
        Returns new annotated IgObject.
    """
    if _all_params_present(igquery) and _all_params_present(igtarget):
        igquery_regions = igquery.regions
        igtarget_regions = igtarget.regions
        df_query = igquery_regions[annotation_type]
        df_target = igtarget_regions[annotation_type]
        df_hybrid = MultiIndex(columns=["Region","Sequence Fragment","Residue","Length"])
        df_hybrid = df_hybrid.append(df_target.loc[df_target['Region'].str.contains('FR1')])
        df_hybrid = df_hybrid.append(df_query.loc[df_query['Region'].str.contains('CDR1')])
        df_hybrid = df_hybrid.append(df_target.loc[df_target['Region'].str.contains('FR2')])
        df_hybrid = df_hybrid.append(df_query.loc[df_query['Region'].str.contains('CDR2')])
        df_hybrid = df_hybrid.append(df_target.loc[df_target['Region'].str.contains('FR3')])
        df_hybrid = df_hybrid.append(df_query.loc[df_query['Region'].str.contains('CDR3')])
        df_hybrid = df_hybrid.append(df_target.loc[df_target['Region'].str.contains('FR4')])
        df_hybrid.reset_index()
        concatenated_seq = _concat_sequence(df_hybrid)
        hybrid_ig_obj = create_annotation(concatenated_seq)
    return hybrid_ig_obj
