from app.core.config import ALLOWED_POLICY_COUNTRIES
from app.schemas.recommendation import (
    RecommendationRequestIn,
    RecommendationResponse,
    RecommendationSummary,
    RequirementItem,
)


class RequirementEngine:
    @staticmethod
    def evaluate(profile: RecommendationRequestIn) -> RecommendationResponse:
        medical = RequirementEngine._check_medical(profile)
        insurance = RequirementEngine._check_insurance(profile)
        requirements = [medical, insurance]

        required_count = sum(1 for item in requirements if item.required)
        optional_count = len(requirements) - required_count

        return RecommendationResponse(
            profile=profile,
            requirements=requirements,
            summary=RecommendationSummary(
                required_count=required_count,
                optional_count=optional_count,
            ),
        )

    @staticmethod
    def _check_medical(profile: RecommendationRequestIn) -> RequirementItem:
        purpose = profile.purpose_of_entry.strip().lower()

        if purpose == "трудовая деятельность":
            return RequirementItem(
                code="medical_examination",
                title="Медицинское освидетельствование",
                required=True,
                deadline="В течение 30 календарных дней со дня въезда либо при обращении с заявлением об оформлении патента или разрешения на работу",
                place="Медицинские организации",
                reason="Цель въезда связана с осуществлением трудовой деятельности",
            )

        if profile.stay_duration_days > 90:
            return RequirementItem(
                code="medical_examination",
                title="Медицинское освидетельствование",
                required=True,
                deadline="В течение 90 календарных дней со дня въезда",
                place="Медицинские организации",
                reason="Срок пребывания превышает 90 суток при цели въезда, не связанной с трудовой деятельностью",
            )

        return RequirementItem(
            code="medical_examination",
            title="Медицинское освидетельствование",
            required=False,
            reason="По введенным данным требование о медицинском освидетельствовании не применяется",
        )

    @staticmethod
    def _check_insurance(profile: RecommendationRequestIn) -> RequirementItem:
        if (
            not profile.has_insurance
            and profile.employment_related
            and profile.citizenship.strip() in ALLOWED_POLICY_COUNTRIES
        ):
            return RequirementItem(
                code="insurance_policy",
                title="Полис обязательного или дополнительного медицинского страхования",
                required=True,
                deadline="Для трудоустройства",
                place="Любая страховая компания в месте пребывания",
                reason="Нет полиса, случай связан с трудоустройством, гражданство входит в установленный перечень стран",
            )

        if profile.has_insurance:
            reason = "У пользователя уже есть полис медицинского страхования"
        elif not profile.employment_related:
            reason = "Рассматриваемый случай не связан с трудоустройством"
        else:
            reason = "Гражданство не входит в перечень стран, для которых по выбранному правилу требуется оформление полиса"

        return RequirementItem(
            code="insurance_policy",
            title="Полис обязательного или дополнительного медицинского страхования",
            required=False,
            reason=reason,
        )
