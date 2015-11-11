from django.db.transaction import atomic
from django.utils.html import strip_tags
from experience.models import Experience, University
from xml.etree import ElementTree

__author__ = 'M.Y'

import psycopg2


@atomic
def go():
    UNIET = ElementTree.parse('experience/b.xml')

    conn = psycopg2.connect("dbname='kalk' user='postgres' host='localhost' password='13712533485'")
    cur = conn.cursor()
    cur.execute("""SELECT * from journalarticle""")
    rows = cur.fetchall()
    for row in rows:
        title = strip_tags(row[13])
        content = row[16]
        group_id = row[3]
        creator = row[6]
        # try:
        #     exp = Experience.objects.get(title=title)
        # except:
        exp = Experience(title=title, confirm=True)

        if group_id == 11047:
            service = 10
        elif group_id == 10715:
            service = 9
        elif group_id == 10837:
            service = 6
        elif group_id == 10777:
            service = 4
        elif group_id == 10747:
            service = 8
        elif group_id == 10732:
            service = 7
        elif group_id == 10762:
            service = 5
        elif group_id == 10792:
            service = 12
        elif group_id == 10670:
            service = 3
        elif group_id == 10807:
            service = 11
        elif group_id == 10852:
            service = 1
        elif group_id == 10822:
            service = 2
        else:
            print("NO SERVICE FOUNDED :(")
            continue

        ET = ElementTree.fromstring(content)

        content = ET.find(".//*[@name='content']").findall('dynamic-content')[0].text

        uni_title = ET.find(".//*[@name='university']").findall('dynamic-content')[0].text
        # uni = University.objects.get_or_create(title=uni_title)[0]

        t = UNIET.find(".//*[@type='%s']" % uni_title)
        if t is not None:
            uni_title = t.attrib['name']

        exp.uni_temp = uni_title
        exp.creator_old = creator

        exp.service = service
        exp.content = content
        exp.save()


MAPPER = {"farhangian yazd": "فرهنگیان یزد", "olompezeshki bioshehr": "علوم پزشکی بوشهر", "amirkabir": "امیرکبیر",
          "boali sina": "بوعلی سینا", "olompezeshki gilan": "علوم پزشکی گیلان",
          "olompezeshki kerman": "علوم پزشکی کرمان",
          "shaid bahonar": "شهید باهنر", "velayat sistan va balochestan": "ولایت سیستان و بلوچستان",
          "razi kermanshah": "رازی کرمانشاه"}


@atomic
def bo():
    for key, val in MAPPER.items():
        Experience.objects.filter(uni_temp=key).update(uni_temp=val)
    # ET = ElementTree.parse('experience/b.xml')
    # for uni in University.objects.all():
    #     t = ET.find(".//*[@type='%s']" % uni.title)
    #     if t is not None:
    #         name = t.attrib['name']
    #         uni.title = name
    #         uni.save()


@atomic
def remove_redundant():
    for content in Experience.objects.values_list('content', flat=True).distinct():
        Experience.objects.filter(pk__in=Experience.objects.filter(content=content).values_list('id', flat=True)[1:]).delete()

@atomic
def change_creators():
    for exp in Experience.objects.all():
        exp.creator_old = "آرشیو کالک"
        exp.save()