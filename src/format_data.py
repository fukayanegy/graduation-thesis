import pandas as pd

def format_data(data):
    required_field = [
            # 売上高
            'jppfs_cor:NetSales',
            'jpcrp_cor:NetSalesSummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults',
            'jpcrp_cor:RevenueIFRSSummaryOfBusinessResults',
            'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults',
            'jppfs_cor:OperatingIncomeINS',
            # 'NetSalesOfCompletedConstructionContractsSummary',

            # 研究開発費
            'jpcrp_cor:ResearchAndDevelopmentExpensesResearchAndDevelopmentActivities',
            'jppfs_cor:ResearchAndDevelopmentExpensesSGA',

            # ROE (自己資本利益率)
            'jpcrp_cor:RateOfReturnOnEquitySummary',
            'jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults',

            # 自己資本比率
            'jpcrp_cor:EquityToAssetRatioSummary',
            'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults',

            # ROA
            'jpcrp_cor:NetAssetsSummary',
            'jpcrp_cor:NetAssetsSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsSummary',
            'jpcrp_cor:TotalAssetsSummaryOfBusinessResults',
            'jppfs_cor:OrdinaryIncome',
            'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults',

            # 取締役人数
            'jpcrp_cor:NumberOfMaleDirectorsAndOtherOfficers',
            'jpcrp_cor:NumberOfFemaleDirectorsAndOtherOfficers',
            'jpcrp_cor:RatioOfFemaleDirectorsAndOtherOfficers',

            # 従業員数/平均年齢/平均勤続年数
            'jpcrp_cor:NumberOfEmployees',
            'jpcrp_cor:AverageAgeYearsInformationAboutReportingCompanyInformationAboutEmployees',
            'jpcrp_cor:AverageLengthOfServiceYearsInformationAboutReportingCompanyInformationAboutEmployees',
            'jpcrp_cor:AverageAnnualSalaryInformationAboutReportingCompanyInformationAboutEmployees',
            ]
    required_context = [
            'CurrentYearInstant',
            'CurrentYearInstant_NonConsolidatedMember',
            'CurrentYearDuration',
            'CurrentYearDuration_NonConsolidatedMember',
            'FilingDateInstant',
            ]
    required_text = [
            'jpcrp_cor:ResearchAndDevelopmentActivitiesTextBlock',
            'jpcrp_cor:ResearchAndDevelopmentExpensesIncludedInGeneralAndAdministrativeExpensesAndManufacturingCostForCurrentPeriodTextBlock',
            # 役員の状況
            'jpcrp_cor:InformationAboutOfficersTextBlock',
            ]
    result = data[
            ((data['ユニットID'].isin(['JPY', 'JPYPerShares', 'pure', 'shares'])) &
            (data['相対年度'].isin(['当期', '当期末', '提出日時点'])) &
            (data['コンテキストID'].isin(required_context)) &
            (data['要素ID'].isin(required_field))) |
            (data['要素ID'].isin(required_text))
            ]
    return result
