import streamlit as st
import pandas as pd
from pathlib import Path


# =========================================================
# 0. 기본 설정
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="기업 추천 시스템",
    page_icon="🏢",
    layout="wide"
)


# =========================================================
# 1. 변수 설정
# =========================================================

FEATURES = [
    "work_life_balance",
    "culture_values",
    "career_opportunities",
    "comp_benefits",
    "senior_management"
]


FEATURE_NAMES_KR = {
    "work_life_balance": "워라밸",
    "culture_values": "기업 문화·가치관",
    "career_opportunities": "성장·커리어 기회",
    "comp_benefits": "보상·복지",
    "senior_management": "경영진·리더십"
}


# Persona 이름과 설명
PERSONA_INFO = {

    "0": {
        "name": "전반 만족·균형형",
        "description": (
            "워라밸, 문화, 성장기회, 보상, 경영진에 대해 "
            "전반적으로 고르게 긍정적인 경험을 보이는 유형입니다."
        ),
        "keywords": "균형 · 안정 · 전반적 만족"
    },

    "1": {
        "name": "문화·보상 중시형",
        "description": (
            "기업 문화와 보상·복지에 대한 만족도가 높은 반면, "
            "성장·커리어 기회와 경영진 평가는 상대적으로 낮은 유형입니다."
        ),
        "keywords": "문화 · 보상 · 복지"
    },

    "2": {
        "name": "성장·문화 중시형",
        "description": (
            "기업 문화와 성장·커리어 기회를 긍정적으로 평가하며, "
            "워라밸보다는 성장 경험을 상대적으로 중요하게 보여주는 유형입니다."
        ),
        "keywords": "성장 · 커리어 · 문화"
    },

    "3": {
        "name": "보상 중심형",
        "description": (
            "보상·복지에 대한 만족도가 상대적으로 높고, "
            "기업 문화와 경영진 경험은 상대적으로 낮게 나타나는 유형입니다."
        ),
        "keywords": "보상 · 실질적 혜택"
    }
}


# =========================================================
# 2. 데이터 불러오기
# =========================================================

try:

    company_profiles = pd.read_csv(
        BASE_DIR / "company_rating_profiles.csv",
        index_col=0
    )

    persona_profiles = pd.read_csv(
        BASE_DIR / "persona_profiles.csv",
        index_col=0
    )

    company_persona = pd.read_csv(
        BASE_DIR / "company_persona_distribution.csv",
        index_col=0
    )

except FileNotFoundError as e:

    st.error(
        "CSV 파일을 찾을 수 없습니다.\n\n"
        "app.py와 CSV 파일 3개가 같은 폴더에 있는지 확인해주세요."
    )

    st.code(str(e))

    st.stop()


# =========================================================
# 3. 메인 화면
# =========================================================

st.title("🏢 나에게 맞는 기업 추천 시스템")

st.write(
    """
    내가 중요하게 생각하는 **직장 선택 기준**을 입력하면  
    실제 직원 리뷰 데이터와 **직원 경험 Persona 분석 결과**를 함께 활용하여
    나에게 상대적으로 잘 맞는 기업을 찾아봅니다.
    """
)

st.success("데이터를 정상적으로 불러왔습니다!")


# =========================================================
# 4. 기업 데이터 표시
# =========================================================

st.subheader("📊 기업별 직원 평가 데이터")

st.caption(
    "각 기업 직원 리뷰를 바탕으로 계산한 5개 직장 경험 항목의 평균 평점입니다."
)

st.dataframe(
    company_profiles.round(3),
    use_container_width=True
)


# =========================================================
# 5. 사용자 중요도 입력
# =========================================================

st.divider()

st.header("🎯 기업을 고를 때, 나는 무엇을 중요하게 볼까?")

st.write(
    """
    아래 점수는 **기업의 점수를 직접 매기는 것이 아니라,**
    내가 기업을 선택할 때 각 요소를 **얼마나 중요하게 생각하는지**를 뜻합니다.

    **1점 = 거의 중요하지 않음 / 5점 = 매우 중요함**
    """
)


col1, col2 = st.columns(2)


with col1:

    work_life_balance = st.slider(
        "⚖️ 워라밸 중요도",
        min_value=1,
        max_value=5,
        value=3,
        step=1
    )

    culture_values = st.slider(
        "🤝 기업 문화·가치관 중요도",
        min_value=1,
        max_value=5,
        value=3,
        step=1
    )

    career_opportunities = st.slider(
        "📈 성장·커리어 기회 중요도",
        min_value=1,
        max_value=5,
        value=3,
        step=1
    )


with col2:

    comp_benefits = st.slider(
        "💰 보상·복지 중요도",
        min_value=1,
        max_value=5,
        value=3,
        step=1
    )

    senior_management = st.slider(
        "👔 경영진·리더십 중요도",
        min_value=1,
        max_value=5,
        value=3,
        step=1
    )


# =========================================================
# 6. 사용자 입력값 저장
# =========================================================

user_weights = pd.Series({

    "work_life_balance": work_life_balance,
    "culture_values": culture_values,
    "career_opportunities": career_opportunities,
    "comp_benefits": comp_benefits,
    "senior_management": senior_management

}, dtype=float)


# =========================================================
# 7. 추천 버튼
# =========================================================

st.write("")

if st.button(
    "🔍 나에게 맞는 기업 찾기",
    type="primary",
    use_container_width=True
):

    # =====================================================
    # 7-1. 내가 선택한 중요도 표시
    # =====================================================

    st.success("입력이 완료되었습니다!")

    st.subheader("📋 내가 선택한 기업 선택 기준")

    preference_df = pd.DataFrame({

        "항목": [
            "워라밸",
            "기업 문화·가치관",
            "성장·커리어 기회",
            "보상·복지",
            "경영진·리더십"
        ],

        "중요도": [
            work_life_balance,
            culture_values,
            career_opportunities,
            comp_benefits,
            senior_management
        ]
    })


    st.dataframe(
        preference_df,
        hide_index=True,
        use_container_width=True
    )


    st.info(
        "이 중요도를 가중치로 사용하여 기업의 실제 직원 평가와 "
        "직원 경험 Persona 구성을 함께 비교합니다."
    )


    # =====================================================
    # 8. 기업 실제 평가 데이터 준비
    # =====================================================

    company_temp = company_profiles.copy()

    if "company" in company_temp.columns:

        company_temp = company_temp.set_index("company")


    company_temp.index = (
        company_temp.index
        .astype(str)
        .str.lower()
        .str.strip()
    )


    company_temp[FEATURES] = (
        company_temp[FEATURES]
        .apply(pd.to_numeric, errors="coerce")
    )


    # =====================================================
    # 9. 중요도를 반영한 기업별 가중 평균 평점
    # =====================================================

    weighted_company_rating = (

        company_temp[FEATURES]

        .mul(
            user_weights,
            axis=1
        )

        .sum(axis=1)

        / user_weights.sum()
    )


    # =====================================================
    # 10. 기업 상대 적합도
    #
    # 단순 절대 평점만 사용하면
    # 기본 평점이 높은 기업이 계속 1위를 할 수 있기 때문에
    #
    # 현재 사용자 중요도에서 나온 가중평균 순위를
    # 0~100 상대점수로 변환
    # =====================================================

    company_rank = (
        weighted_company_rating
        .rank(
            ascending=False,
            method="first"
        )
    )


    number_of_companies = len(
        weighted_company_rating
    )


    company_relative_score = (

        (
            number_of_companies
            - company_rank
            + 1
        )

        / number_of_companies

        * 100
    )


    # =====================================================
    # 11. Persona 데이터 준비
    # =====================================================

    persona_temp = persona_profiles.copy()

    if "persona_cluster" in persona_temp.columns:

        persona_temp = (
            persona_temp
            .set_index("persona_cluster")
        )


    persona_temp.index = (
        persona_temp.index
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.strip()
    )


    persona_temp[FEATURES] = (
        persona_temp[FEATURES]
        .apply(pd.to_numeric, errors="coerce")
    )


    # =====================================================
    # 12. 사용자의 중요도와 각 Persona의 적합도
    # =====================================================

    persona_fit = (

        persona_temp[FEATURES]

        .mul(
            user_weights,
            axis=1
        )

        .sum(axis=1)

        / user_weights.sum()

        / 5

        * 100
    )


    # =====================================================
    # 13. 회사별 Persona 구성비 데이터 준비
    # =====================================================

    persona_dist = company_persona.copy()

    if "company" in persona_dist.columns:

        persona_dist = (
            persona_dist
            .set_index("company")
        )


    persona_dist.index = (
        persona_dist.index
        .astype(str)
        .str.lower()
        .str.strip()
    )


    # 열 이름 정리
    clean_columns = []

    for col in persona_dist.columns:

        clean_col = (
            str(col)
            .replace("persona_", "")
            .replace("Persona_", "")
            .replace("Persona ", "")
            .replace(".0", "")
            .strip()
        )

        clean_columns.append(
            clean_col
        )


    persona_dist.columns = clean_columns


    persona_dist = (
        persona_dist
        .apply(
            pd.to_numeric,
            errors="coerce"
        )
    )


    # CSV가 0~100 형태이면 0~1로 변환
    if persona_dist.max().max() > 1.5:

        persona_dist = (
            persona_dist / 100
        )


    # =====================================================
    # 14. 회사별 Persona 적합도 계산
    # =====================================================

    common_personas = [

        persona

        for persona in persona_dist.columns

        if persona in persona_fit.index
    ]


    if len(common_personas) == 0:

        st.error(
            "Persona 데이터의 열 이름을 서로 연결하지 못했습니다."
        )

        st.stop()


    persona_score = (

        persona_dist[
            common_personas
        ]

        .mul(
            persona_fit[
                common_personas
            ],
            axis=1
        )

        .sum(axis=1)
    )


    # =====================================================
    # 15. 최종 추천 점수
    #
    # 기업 실제 평가 기반 상대 적합도 : 60%
    # Persona 구성 적합도            : 40%
    # =====================================================

    recommendation = pd.concat(

        [

            weighted_company_rating.rename(
                "weighted_rating"
            ),

            company_relative_score.rename(
                "direct_score_100"
            ),

            persona_score.rename(
                "persona_score_100"
            )

        ],

        axis=1

    ).dropna()


    recommendation["final_score"] = (

        recommendation[
            "direct_score_100"
        ] * 0.60

        +

        recommendation[
            "persona_score_100"
        ] * 0.40
    )


    recommendation = (

        recommendation

        .sort_values(
            "final_score",
            ascending=False
        )

        .reset_index()
    )


    recommendation = recommendation.rename(

        columns={
            recommendation.columns[0]: "company"
        }

    )


    recommendation.insert(

        0,

        "rank",

        range(
            1,
            len(recommendation) + 1
        )
    )


    # =====================================================
    # 16. 추천 결과
    # =====================================================

    st.divider()

    st.header("🏆 나에게 맞는 기업 추천 결과")


    top_company = (
        recommendation
        .iloc[0]["company"]
    )


    top_score = (
        recommendation
        .iloc[0]["final_score"]
    )


    st.success(
        f"🥇 현재 입력한 조건에서 가장 적합한 기업은 "
        f"**{str(top_company).upper()}** 입니다. "
        f"최종 적합도는 **{top_score:.1f}점**입니다."
    )


    result_table = (

        recommendation[
            [
                "rank",
                "company",
                "weighted_rating",
                "direct_score_100",
                "persona_score_100",
                "final_score"
            ]
        ]

        .copy()
    )


    result_table.columns = [

        "순위",
        "기업",
        "가중 평균 평점",
        "기업 상대 적합도",
        "Persona 적합도",
        "최종 추천 점수"

    ]


    st.dataframe(

        result_table.round(2),

        hide_index=True,

        use_container_width=True
    )


    # =====================================================
    # 17. 기업별 최종 적합도 그래프
    # =====================================================

    st.subheader("📊 기업별 최종 적합도")


    company_chart = (

        recommendation[
            [
                "company",
                "final_score"
            ]
        ]

        .set_index("company")
    )


    company_chart.columns = [
        "최종 추천 점수"
    ]


    st.bar_chart(
        company_chart
    )


    # =====================================================
    # 18. Persona 분석
    # =====================================================

    st.divider()

    st.header("🧩 나와 가까운 직원 경험 Persona")


    user_persona = (
        persona_fit
        .idxmax()
    )


    user_persona_key = (
        str(user_persona)
        .replace(".0", "")
    )


    user_persona_name = (

        PERSONA_INFO
        .get(
            user_persona_key,
            {
                "name": f"Persona {user_persona_key}"
            }
        )
        ["name"]
    )


    st.success(
        f"현재 입력한 중요도와 가장 가까운 유형은 "
        f"**Persona {user_persona_key} — "
        f"{user_persona_name}** 입니다."
    )


    # Persona 적합도 그래프
    persona_fit_display = pd.DataFrame({

        "적합도": persona_fit

    })


    persona_labels = []

    for persona_id in persona_fit_display.index:

        persona_key = (
            str(persona_id)
            .replace(".0", "")
        )

        persona_name = (

            PERSONA_INFO
            .get(
                persona_key,
                {
                    "name": f"Persona {persona_key}"
                }
            )
            ["name"]
        )

        persona_labels.append(
            f"Persona {persona_key} · {persona_name}"
        )


    persona_fit_display.index = (
        persona_labels
    )


    st.subheader("📈 Persona별 현재 입력 적합도")


    st.bar_chart(
        persona_fit_display
    )


    # =====================================================
    # 19. Persona 설명표
    # =====================================================

    st.subheader("📘 Persona는 각각 어떤 유형일까?")


    persona_description_rows = []


    for persona_id in sorted(
        PERSONA_INFO.keys()
    ):

        info = (
            PERSONA_INFO[
                persona_id
            ]
        )


        fit_value = None


        if persona_id in persona_fit.index:

            fit_value = (
                persona_fit[
                    persona_id
                ]
            )


        persona_description_rows.append({

            "Persona": (
                f"Persona {persona_id}"
            ),

            "유형": (
                info["name"]
            ),

            "주요 특징": (
                info["keywords"]
            ),

            "설명": (
                info["description"]
            ),

            "현재 입력 기준 적합도": (
                round(
                    fit_value,
                    1
                )
                if fit_value is not None
                else "-"
            )

        })


    persona_description_df = (
        pd.DataFrame(
            persona_description_rows
        )
    )


    st.dataframe(

        persona_description_df,

        hide_index=True,

        use_container_width=True
    )


    # =====================================================
    # 20. 최종 추천 이유 자동 생성
    # =====================================================

    st.divider()

    st.header("💡 왜 이 기업이 나에게 추천됐을까?")


    # -----------------------------------------------------
    # 20-1. 1위 기업 실제 평가
    # -----------------------------------------------------

    top_company_key = (
        str(top_company)
        .lower()
        .strip()
    )


    top_company_ratings = (

        company_temp

        .loc[
            top_company_key,
            FEATURES
        ]

        .astype(float)
    )


    # -----------------------------------------------------
    # 20-2. 중요도 × 실제 기업 평점
    #
    # 가장 추천 점수에 크게 기여한 항목 찾기
    # -----------------------------------------------------

    weighted_strength = (

        top_company_ratings
        * user_weights
    )


    top_features = (

        weighted_strength

        .sort_values(
            ascending=False
        )

        .index[:2]

        .tolist()
    )


    feature_1 = top_features[0]
    feature_2 = top_features[1]


    feature_1_name = (
        FEATURE_NAMES_KR[
            feature_1
        ]
    )


    feature_2_name = (
        FEATURE_NAMES_KR[
            feature_2
        ]
    )


    feature_1_rating = (
        top_company_ratings[
            feature_1
        ]
    )


    feature_2_rating = (
        top_company_ratings[
            feature_2
        ]
    )


    feature_1_importance = (
        user_weights[
            feature_1
        ]
    )


    feature_2_importance = (
        user_weights[
            feature_2
        ]
    )


    # -----------------------------------------------------
    # 20-3. 1위 기업의 사용자 Persona 비율
    # -----------------------------------------------------

    persona_share_text = ""


    if (
        top_company_key
        in persona_dist.index
        and
        user_persona_key
        in persona_dist.columns
    ):

        persona_share = (

            persona_dist.loc[
                top_company_key,
                user_persona_key
            ]

            * 100
        )


        persona_share_text = (
            f"또한 **{str(top_company).upper()}**의 직원 리뷰에서는 "
            f"당신과 가장 가까운 **Persona {user_persona_key} "
            f"({user_persona_name})** 유형이 "
            f"약 **{persona_share:.1f}%**를 차지합니다."
        )


    # -----------------------------------------------------
    # 20-4. 최종 설명
    # -----------------------------------------------------

    st.markdown(
        f"""
### 🥇 {str(top_company).upper()} 추천 이유

현재 입력한 **기업 선택 기준**과 실제 직원 리뷰 데이터를 함께 비교한 결과,  
**{str(top_company).upper()}**이 가장 높은 최종 적합도를 보였습니다.

특히 현재 선택에서 추천 점수에 크게 기여한 항목은 다음과 같습니다.

**① {feature_1_name}**  
- 내가 설정한 중요도: **{feature_1_importance:.0f} / 5**
- {str(top_company).upper()} 직원 평균 평가: **{feature_1_rating:.2f} / 5**

**② {feature_2_name}**  
- 내가 설정한 중요도: **{feature_2_importance:.0f} / 5**
- {str(top_company).upper()} 직원 평균 평가: **{feature_2_rating:.2f} / 5**

당신의 중요도 패턴과 가장 가까운 직원 경험 유형은  
**Persona {user_persona_key} — {user_persona_name}** 입니다.

{persona_share_text}

따라서 이 추천 결과는 단순히 전체 평점이 높은 기업을 고른 것이 아니라,

**나의 선택 기준 → 기업의 실제 직원 평가 → 직원 경험 Persona 구성**

을 차례로 결합하여 계산한 결과입니다.
        """
    )


    # =====================================================
    # 21. 점수 구성 설명
    # =====================================================

    with st.expander(
        "🔎 최종 추천 점수는 어떻게 계산되나요?"
    ):

        st.write(
            """
            **기업 상대 적합도 60% + Persona 적합도 40%**

            - **가중 평균 평점**  
              사용자가 중요하게 선택한 항목에 더 큰 가중치를 주어
              각 기업의 직원 평가를 계산합니다.

            - **기업 상대 적합도**  
              현재 입력 조건에서 기업들의 가중 평균 평점을 서로 비교한
              상대 점수입니다.

            - **Persona 적합도**  
              사용자의 중요도와 잘 맞는 직원 경험 Persona가
              해당 기업에 얼마나 분포하는지를 반영합니다.

            - **최종 추천 점수**  
              위 두 정보를 결합한 추천용 종합 지표입니다.
            """
        )


    st.caption(
        "※ 본 결과는 제공된 직원 리뷰 데이터에 기반한 탐색용 추천 결과이며, "
        "기업의 절대적인 우열을 의미하지 않습니다."
    )