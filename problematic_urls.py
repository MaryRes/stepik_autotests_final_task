

class ProblematicUrls:
    """
    Class to store known problematic URLs.
    """

    UI_BUGS = {'product_name_bug': 'http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer7'}

    ALL_PROBLEMATIC_URLS = {
        **UI_BUGS
    }

    @staticmethod
    def get_urls_by_severity(severity="all"):
        """Get URLs based on the severity level."""
        severities = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": ["product_name_bug"]
        }

        if severity == "all":
            return ProblematicUrls.ALL_PROBLEMATIC_URLS
        else:
            return {k: ProblematicUrls.ALL_PROBLEMATIC_URLS[k] for k in severities.get(severity, [])}