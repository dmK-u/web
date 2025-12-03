<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" indent="yes"/>

    <xsl:template match="/">
        <html>
            <head>
                <title>Address Book Export</title>
                <style>
                    /* Basic CSS to make it look nice */
                    body { font-family: sans-serif; background-color: #f4f4f4; padding: 20px; }
                    .container { display: flex; flex-wrap: wrap; gap: 20px; }
                    .card {
                        background: white;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                        padding: 20px;
                        width: 300px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }
                    h2 { margin-top: 0; color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
                    .label { font-weight: bold; color: #555; text-transform: capitalize; }
                    .group { margin-bottom: 15px; }
                    ul { list-style-type: none; padding: 0; margin: 0; }
                    li { margin-bottom: 5px; }
                </style>
            </head>
            <body>
                <h1>Address Book</h1>
                <div class="container">
                    <xsl:for-each select="addressbook/address">
                        <div class="card">
                            <h2><xsl:value-of select="name"/>&#160;<xsl:value-of select="lastname"/></h2>
                            
                            <div class="group">
                                <div class="label">Contact Numbers:</div>
                                <ul>
                                    <xsl:for-each select="phone">
                                        <li>
                                            <span class="label" style="font-size:0.9em; color:#888;">
                                                <xsl:value-of select="@type"/>: 
                                            </span>
                                            <xsl:value-of select="."/>
                                        </li>
                                    </xsl:for-each>
                                </ul>
                            </div>

                            <div class="group">
                                <div class="label">
                                    Location (<xsl:value-of select="location/@type"/>):
                                </div>
                                <div><xsl:value-of select="location/street"/></div>
                                <div>
                                    <xsl:value-of select="location/poc"/>&#160;<xsl:value-of select="location/city"/>
                                </div>
                            </div>
                        </div>
                    </xsl:for-each>
                </div>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>
